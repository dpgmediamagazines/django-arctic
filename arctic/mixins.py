"""
Basic mixins for generic class based views.
"""

from __future__ import (absolute_import, unicode_literals)

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured

from .models import (Role, UserRole)


class SuccessMessageMixin(object):
    """
    Adds a success message on successful form submission.
    Altered to work with extra_views
    """
    success_message = ''

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def forms_valid(self, form, inlines):
        response = super(SuccessMessageMixin, self).forms_valid(form, inlines)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            object=self.object,
        )


class LinksMixin(object):
    """
    Adding links to view, to be resolved with 'arctic_url' template tag
    """
    def get_links(self):
        if not self.links:
            return None
        else:
            allowed_links = []
            for link in self.links:
                allowed_links.append(link)
            return allowed_links


class LayoutMixin(object):
    """
    Adding customizable fields to view. Using the 12-grid system, you
    can now give fields a css-attribute.

    layout = ('field1', ('field2', 'field3'))
    layout = ('field1|6', ('field2|max', 'field3|min'))
    layout = {
        'fieldset1': ('field1, field2'),
        '-fieldset2|some description here': ('field3', ('field4', 'field5')),
        '-fieldset3': ('field6, field7')
    }

    INPUT:
    layout = {'0_my_fieldsettt': ('title|10', ('category', 'updated_at|4')),
              '1_new_fieldset': ('published|4')}

    OUTPUT
    layout = {'0_my_fieldsettt': {1: [{'class': '10',
                                     'field': <django.forms.boundfield.BoundField>,
                                     'name': 'title'}],
                                2: [{'class': None,
                                     'field': <django.forms.boundfield.BoundField>,
                                     'name': 'category'},
                                    {'class': '4',
                                     'field': <django.forms.boundfield.BoundField>,
                                     'name': 'updated_at'}]},
            '1_new_fieldset': {1: [{'class': '4',
                                    'field': <django.forms.boundfield.BoundField>,
                                    'name': 'published'}]}},
    """
    _fields = None

    def get_layout(self):
        try:
            self.layout
        except AttributeError:
            return None

        fieldsets = {}
        self._fields = self.get_form().fields

        if isinstance(self.layout, dict):
            for key, row in self.layout.items():
                try:
                    key_to_int = int(key)
                    key = "key_%d" % key_to_int     # return key which is easily matched in template
                except ValueError:
                    pass
                except TypeError:
                    pass

                if isinstance(row, str):
                    # If there is just one element in a fieldset, just return that one field
                    _field = self._return_field(row)
                    if not _field:
                        continue
                    fieldsets[key] = {1: [_field]}  # Items are indexed by one. Not that it matters
                else:
                    # use numbers to preserve order. This only works up to 10 fieldsets
                    fieldsets[key] = self._process_rows(row)

        if isinstance(self.layout, str):
            fieldsets[0] = {0: [self._return_field(self.layout)]}
        elif isinstance(self.layout, tuple):
            fieldsets[0] = self._process_rows(self.layout)

        return fieldsets

    def _process_rows(self, rows):
        allowed_rows = {}
        for row in rows:
            if isinstance(row, tuple):
                _row = []
                for field in row:
                    _field = self._return_field(field)
                    if _field:
                        _row.append(_field)

                if len(_row) == 0:
                    pass
                elif len(_row) == 1:
                    _field = self._return_field(row[0])
                    if _field:
                        allowed_rows[len(allowed_rows) + 1] = [_field]
                else:
                    allowed_rows[len(allowed_rows) + 1] = _row

            if isinstance(row, str):
                _field = self._return_field(row)
                if _field:
                    allowed_rows[len(allowed_rows) + 1] = [_field]

        return allowed_rows

    def _return_field(self, field):
        field_name, field_class = self._split_str(field)
        if field_name in self._fields:
            return {
                'name': field_name,
                'class': field_class,
                'field': self.get_form()[field_name],
            }
        else:
            return None

    def _split_str(self, field):
        items = field.split('|')
        if len(items) == 2:
            return items[0], items[1]
        elif len(items) == 1:
            return items[0], None


class RoleAuthentication():
    """
    This class adds a role relation to the standard django auth user to add
    support for role based permissions in any class - usually a View.
    """
    required_permission = None
    ADMIN = 'admin'

    @classmethod
    def sync(cls):
        """
        Save all the roles defined in the settings that are not yet in the db
        this is needed to create a foreign key relation between a user and a
        role. Roles that are no longer specified in settings are set as
        inactive.
        """

        try:
            settings_roles = set(settings.ARCTIC_ROLES.keys())
        except AttributeError:
            settings_roles = set()

        saved_roles = set(Role.objects.values_list('name', flat=True))
        unsaved_roles = settings_roles - saved_roles
        unused_roles = saved_roles - settings_roles - set([cls.ADMIN])

        # ensure that admin is not defined in settings
        if cls.ADMIN in settings_roles:
            raise ImproperlyConfigured('"' + cls.ADMIN + '" role is reserved '
                                       'and cannot be defined in settings')

        # ensure that admin exists in the database
        if cls.ADMIN not in saved_roles:
            Role(name=cls.ADMIN, is_active=True).save()

        # check if the role defined in settings already exists in the database
        # and if it does ensure it is enabled.
        for role in saved_roles:
            if role in settings_roles:
                saved_role = Role.objects.get(name=role)
                if not saved_role.is_active:
                    saved_role.is_active = True
                    saved_role.save()

        for role in unsaved_roles:
            Role(name=role).save()

        for role in unused_roles:
            unused_role = Role.objects.get(name=role)
            unused_role.is_active = False
            unused_role.save()

    def has_perm(self, user):
        if not self.required_permission:
            return True
        role = UserRole.objects.get(user=user).role.name
        if role == self.ADMIN:
            return True
        result = self.required_permission in settings.ARCTIC_ROLES[role]
        # will try to call a method with the same name as the permission
        # to enable an object level permission check.
        if result:
            try:
                return getattr(self, self.required_permission)(role)
            except AttributeError:
                pass
        return result
