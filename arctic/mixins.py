"""
Basic mixins for generic class based views.
"""

from __future__ import (absolute_import, unicode_literals)

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.forms import model_to_dict

from collections import OrderedDict

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
    can now give fields a css-attribute. See reference for more information
    """
    _fields = []
    ALLOWED_COLUMNS = 12        # There is a 12 grid system

    def get_layout(self):
        try:
            self.layout
        except AttributeError:
            return None

        self._get_fields()

        allowed_rows = OrderedDict()
        if isinstance(self.layout, OrderedDict):
            for fieldset, rows in self.layout.items():
                fieldset = self._return_fieldset(fieldset)

                if isinstance(rows, str):
                    allowed_rows[fieldset] = [rows]
                else:
                    row = self._process_row_with_fieldset(rows)
                    allowed_rows[fieldset] = row

        elif isinstance(self.layout, list) or isinstance(self.layout, tuple):
            row = self._process_row(self.layout)
            allowed_rows[0] = row

        else:
            raise ImproperlyConfigured('LayoutMixin expects a list/tuple or '
                                       'an OrderedDict')

        return allowed_rows

    def _get_fields(self):
        mtd = model_to_dict(self.object)
        self._fields = [field
                       for field, val in mtd.items()]

    def _return_fieldset(self, fieldset):
        if fieldset.count('|') > 1:
            raise ImproperlyConfigured('The fieldset name does not support '
                                       'more than one | sign. It\'s meant to '
                                       'separate a fieldset from it\'s '
                                       'description.')
        if fieldset[1] == '-':
            fieldset = '{fieldset}_collapse'.format(fieldset=fieldset[1:])
        if '|' in fieldset:
            splitted_text = fieldset.split('|')
            fieldset_description = splitted_text[1]
            fieldset = fieldset_description
        return fieldset

    def _process_row_with_fieldset(self, rows):
        allowed_rows = []
        for row in rows:
            if isinstance(row, str):
                allowed_rows.append(self._return_field(row))
            elif isinstance(row, list) or isinstance(row, tuple):
                rows = self._process_row(row)
                allowed_rows.append(rows)
        return allowed_rows

    def _process_row(self, row):
        row_as_dict = {}        # use this to preserve order of fields in row
        has_column = {}
        has_no_column = {}
        sum_existing_column = 0

        rows_to_dict = {}
        for index, field in enumerate(row):
            row_as_dict[index] = field

            # Yeah, like this isn't incomprehensible yet. Let's add recursion
            if isinstance(field, list):
                rows_to_dict[index] = self._process_row(field)
                continue

            name, column = self._split_str(field)
            if column:
                has_column[index] = self._return_field(field)
                sum_existing_column += int(column)
            else:
                has_no_column[index] = field

        col_avg, col_last = self._calc_avg_and_last_val(has_no_column,
                                                        sum_existing_column)

        # Regenerate has_no_column by adding the amount of columns at the end
        for index, col in has_no_column.items():
            if index == len(has_no_column):
                field_name = '{col}|{col_last}'.format(col=col,
                                                      col_last=col_last)
                has_no_column[index] = self._return_field(field_name)
            else:
                field_name = '{col}|{col_avg}'.format(col=col,
                                                     col_avg=col_avg)
                has_no_column[index] = self._return_field(field_name)

        # Merge it all back together to a dict, to preserve the order
        for index, field in row_as_dict.items():
            if index in has_column:
                rows_to_dict[index] = has_column[index]
            if index in has_no_column:
                rows_to_dict[index] = has_no_column[index]

        rows_to_list = [field
                        for index, field in rows_to_dict.items()]

        return rows_to_list

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
        """ Split title|7 into (title, 7) """
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
