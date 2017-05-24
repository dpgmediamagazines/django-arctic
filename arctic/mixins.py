"""
Basic mixins for generic class based views.
"""

from __future__ import (absolute_import, unicode_literals)

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import (ImproperlyConfigured, PermissionDenied)
from django.core.urlresolvers import reverse
from django.utils import six

from collections import OrderedDict

from arctic.loading import (get_role_model, get_user_role_model)
from arctic.utils import view_from_url
from arctic.widgets import SelectAutoComplete

Role = get_role_model()
UserRole = get_user_role_model()


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

                # check permission based on named_url
                if not view_from_url(link[1]).\
                        has_permission(self.request.user):
                    continue

                allowed_links.append(link)
            return allowed_links


class LayoutMixin(object):
    """
    Adding customizable fields to view. Using the 12-grid system, you
    can now give fields a css-attribute. See reference for more information

    This is how layouts are built:
        Fieldset
          |-->  Rows
                  |--> Fields
    """
    layout = None
    _fields = []
    readonly_fields = None
    ALLOWED_COLUMNS = 12        # There are 12 columns available

    def get_layout(self):
        if not self.layout:
            return None

        self._get_fields()

        allowed_rows = OrderedDict()
        i = 0
        if type(self.layout) is OrderedDict:
            for fieldset, rows in self.layout.items():
                fieldset = self._return_fieldset(fieldset)
                if isinstance(rows, six.string_types) or \
                        isinstance(rows, six.text_type):
                    allowed_rows.update({i: {'fieldset': fieldset,
                                             'rows': rows}})
                else:
                    row = self._process_first_level(rows)
                    allowed_rows.update({i: {'fieldset': fieldset,
                                             'rows': row}})
                i += 1

        elif type(self.layout) in (list, tuple):
            row = self._process_first_level(self.layout)
            fieldset = self._return_fieldset(0)
            allowed_rows.update({i: {'fieldset': fieldset,
                                     'rows': row}})

        else:
            raise ImproperlyConfigured('LayoutMixin expects a list/tuple or '
                                       'an OrderedDict')

        return allowed_rows

    def _get_fields(self):
        self._fields = [field for field in self.get_form().fields]

    def _process_first_level(self, rows):
        allowed_rows = []
        for row in rows:
            if isinstance(row, six.string_types) or \
                    isinstance(row, six.text_type):
                allowed_rows.append(self._return_field(row))
            elif type(row) in (list, tuple):
                rows = self._process_row(row)
                allowed_rows.append(rows)
        return allowed_rows

    def _process_row(self, row):
        has_column = {}
        has_no_column = {}
        sum_existing_column = 0

        _row = {}
        for index, field in enumerate(row):
            # Yeah, like this isn't incomprehensible yet. Let's add recursion
            if type(field) in (list, OrderedDict):
                _row[index] = self._process_row(field)
            elif isinstance(field, six.string_types) or \
                    isinstance(field, six.text_type):
                name, column = self._split_str(field)
                if column:
                    has_column[index] = self._return_field(field)
                    sum_existing_column += int(column)
                else:
                    has_no_column[index] = field

        col_avg, col_last = self._calc_avg_and_last_val(has_no_column,
                                                        sum_existing_column)
        has_no_column = self._set_has_no_columns(has_no_column,
                                                 col_avg,
                                                 col_last)

        # Merge it all back together to a dict, to preserve the order
        for index, field in enumerate(row):
            if index in has_column:
                _row[index] = has_column[index]
            if index in has_no_column:
                _row[index] = has_no_column[index]

        rows_to_list = [field
                        for index, field in _row.items()]

        return rows_to_list

    def _set_has_no_columns(self, has_no_column, col_avg, col_last):
        """
        Regenerate has_no_column by adding the amount of columns at the end
        """
        for index, field in has_no_column.items():
            if index == len(has_no_column):
                field_name = '{field}|{col_last}'.format(field=field,
                                                         col_last=col_last)
                has_no_column[index] = self._return_field(field_name)
            else:
                field_name = '{field}|{col_avg}'.format(field=field,
                                                        col_avg=col_avg)
                has_no_column[index] = self._return_field(field_name)
        return has_no_column

    def _return_fieldset(self, fieldset):
        """
        This function became a bit messy, since it needs to deal with two
        cases.

        1) No fieldset, which is represented as an integer
        2) A fieldset
        """
        collapsible = False
        description = None
        try:
            # Make sure strings with numbers work as well, do this
            int(fieldset)
            title = None
        except ValueError:
            if fieldset.count('|') > 1:
                raise ImproperlyConfigured('The fieldset name does not '
                                           'support more than one | sign. '
                                           'It\'s meant to separate a '
                                           'fieldset from it\'s '
                                           'description.')

            title = fieldset
            if fieldset and fieldset[0] == '-':
                collapsible = True
                title = fieldset[1:]
            if '|' in fieldset:
                title, description = fieldset.split('|')

        return {'title': title,
                'description': description,
                'collapsible': collapsible}

    def _calc_avg_and_last_val(self, has_no_column, sum_existing_columns):
        """
        Calculate the average of all columns and return a rounded down number.
        Store the remainder and add it to the last row. Could be implemented
        better. If the enduser wants more control, he can also just add the
        amount of columns. Will work fine with small number (<4) of items in a
        row.

        :param has_no_column:
        :param sum_existing_columns:
        :return: average, columns_for_last_element
        """
        sum_no_columns = len(has_no_column)
        columns_left = self.ALLOWED_COLUMNS - sum_existing_columns

        if sum_no_columns == 0:
            columns_avg = columns_left
        else:
            columns_avg = int(columns_left / sum_no_columns)

        remainder = columns_left - (columns_avg * sum_no_columns)
        columns_for_last_element = columns_avg + remainder
        return columns_avg, columns_for_last_element

    def _split_str(self, field):
        """
        Split title|7 into (title, 7)
        """
        field_items = field.split('|')
        if len(field_items) == 2:
            return field_items[0], field_items[1]
        elif len(field_items) == 1:
            return field_items[0], None

    def _return_field(self, field):
        field_name, field_class = self._split_str(field)
        if field_name in self._fields:
            return {
                'name': field_name,
                'column': field_class,
                'field': self.get_form()[field_name],
            }
        else:
            return None

    def update_form_fields(self, form):
        for field in form.fields:
            if form.fields[field].__class__.__name__ == 'ModelChoiceField':
                for key, values in settings.ARCTIC_AUTOCOMPLETE.items():
                    field_cls = '.'.join(values[0].lower().split('.')[-2:])
                    if field_cls == str(form.fields[field].queryset.
                                        model._meta):
                        url = reverse('autocomplete', args=[key, ''])
                        choices = ()
                        if form.instance.pk:
                            field_id = getattr(form.instance, field +
                                               '_id')
                            field_value = getattr(form.instance, field)
                            choices = ((field_id, field_value),)
                        form.fields[field].widget = SelectAutoComplete(
                            attrs={'url': url,
                                   'class': 'js-selectize-autocomplete'},
                            choices=choices)
            if self.readonly_fields and field in self.readonly_fields:
                form.fields[field].widget.attrs['readonly'] = True
        return form

    def get_form(self, form_class=None):
        form = super(LayoutMixin, self).get_form(form_class=None)
        try:
            form = self.update_form_fields(form)
        except AttributeError:
            pass
        return form

    def get_context_data(self, **kwargs):
        context = super(LayoutMixin, self).get_context_data(**kwargs)
        try:
            i = 0
            for formset in context['inlines']:
                j = 0
                if not hasattr(context['inlines'][i], 'verbose_name'):
                    setattr(context['inlines'][i], 'verbose_name',
                            formset.model._meta.verbose_name_plural)
                for form in formset:
                    context['inlines'][i][j].fields = \
                        self.update_form_fields(form).fields
                    j += 1
                i += 1
        except KeyError:
            pass
        return context


class RoleAuthentication(object):
    """
    This class adds a role relation to the standard django auth user to add
    support for role based permissions in any class - usually a View.
    """
    ADMIN = 'admin'
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request.user):
            raise PermissionDenied()
        return super(RoleAuthentication, self).dispatch(
            request, *args, **kwargs)

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

    @classmethod
    def get_permission_required(cls):
        """
        Get permission required property.
        Must return an iterable.
        """
        if cls.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. '
                'Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(cls.__name__)
            )
        if isinstance(cls.permission_required, six.string_types):
            if cls.permission_required != "":
                perms = (cls.permission_required,)
            else:
                perms = ()
        else:
            perms = cls.permission_required

        return perms

    @classmethod
    def has_permission(cls, user):
        """
        We override this method to customize the way permissions are checked.
        Using our roles to check permissions.
        """
        # no login is needed, so its always fine
        if not cls.requires_login:
            return True

        # if user is somehow not logged in
        if not user.is_authenticated():
            return False

        # attribute permission_required is mandatory, returns tuple
        perms = cls.get_permission_required()
        # if perms are defined and empty, we skip checking
        if not perms:
            return True

        # get role of user, skip admin role
        role = user.urole.role.name
        if role == cls.ADMIN:
            return True

        # check if at least one permissions is valid
        for permission in perms:
            if cls.check_permission(role, permission):
                return True

        # permission denied
        return False

    @classmethod
    def check_permission(cls, role, permission):
        """
        Check if role contains permission
        """
        result = permission in settings.ARCTIC_ROLES[role]
        # will try to call a method with the same name as the permission
        # to enable an object level permission check.
        if result:
            try:
                return getattr(cls, permission)(role)
            except AttributeError:
                pass
        return result


class FormMediaMixin(object):
    """
    Gathers media assets defined in forms
    """

    @property
    def media(self):
        # Why not simply call super? Just
        # to have custom media defined at the bottom,
        # since order matters here.
        media = self._get_common_media()
        media += self._get_view_media()
        media += self._get_form_media()
        media += self.get_media_assets()

        return media

    def _get_form_media(self):
        form = self.get_form()
        return getattr(form, 'media', None)
