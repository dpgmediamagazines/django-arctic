"""
Basic mixins for generic class based views.
"""

import importlib

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import (ImproperlyConfigured, PermissionDenied)
from django.template import (Template, Context)
from django.urls import reverse
from django.utils import six

from collections import OrderedDict

from .forms import SimpleSearchForm
from .loading import (get_role_model, get_user_role_model)
from .utils import (arctic_setting, reverse_url, view_from_url)
from .widgets import SelectizeAutoComplete

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


class FormMixin(object):
    """
    Adding customizable fields to view. Using the 12-grid system, you
    can now give fields a css-attribute. See reference for more information

    This is how layouts are built:
        Fieldset
          |-->  Rows
                  |--> Fields
    """
    use_widget_overloads = True
    layout = None
    _fields = []
    links = None             # Optional links such as list of linked items
    readonly_fields = None
    ALLOWED_COLUMNS = 12     # There are 12 columns available

    def get_links(self):
        if not self.links:
            return None

        allowed_links = []
        for link in self.links:

            # check permission based on named_url
            if not view_from_url(link[1]).has_permission(self.request.user):
                continue

            try:
                obj = self.get_object()
            except AttributeError:
                obj = None
            allowed_links.append({
                'label': link[0],
                'url': reverse_url(link[1], obj)})
        return allowed_links

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
        collapsible = None
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
                                           'fieldset from its description.')

            title = fieldset
            if '|' in fieldset:
                title, description = fieldset.split('|')
            if fieldset and (fieldset[0] in '-+'):
                if fieldset[0] == '-':
                    collapsible = 'closed'
                else:
                    collapsible = 'open'
                title = title[1:]

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
        widget_overloads = arctic_setting('ARCTIC_WIDGET_OVERLOADS')
        widgets_to_be_overloaded = widget_overloads.keys()
        if hasattr(form, 'form_classes'):
            form_names = form.form_classes.keys()
            for form_name in form_names:
                new_form = self._update_form_fields(
                    form[form_name], widget_overloads,
                    widgets_to_be_overloaded)
                setattr(form, form_name, new_form)
            return form

        return self._update_form_fields(form, widget_overloads,
                                        widgets_to_be_overloaded)

    def _update_form_fields(self, form, widget_overloads,
                            widgets_to_be_overloaded):
        for field in form.fields:
            if self.use_widget_overloads:
                widget_class = form.fields[field].widget.__class__.__name__
                if widget_class in widgets_to_be_overloaded:
                    module, wdgt = widget_overloads[widget_class].\
                        rsplit('.', 1)
                    new_widget_module = importlib.import_module(module)
                    new_widget_class = getattr(new_widget_module, wdgt)
                    new_widget = None
                    if widget_class in ('Select', 'SelectMultiple',
                                        'ToggleSelectWidget', 'LazySelect'):
                        new_widget = new_widget_class(
                            form.fields[field].widget.attrs,
                            form.fields[field].widget.choices)
                    elif widget_class in ('DateInput', 'DateTimeInput',
                                          'TimeInput'):
                        new_widget = new_widget_class(
                            form.fields[field].widget.attrs,
                            form.fields[field].widget.format)
                        new_widget.supports_microseconds = \
                            form.fields[field].widget.supports_microseconds
                    else:
                        new_widget = new_widget_class(
                            form.fields[field].widget.attrs)
                    form.fields[field].widget = new_widget

            field_class_name = form.fields[field].__class__.__name__
            if field_class_name == 'ModelChoiceField' and \
               hasattr(settings, 'ARCTIC_AUTOCOMPLETE'):
                for key, values in settings.ARCTIC_AUTOCOMPLETE.items():
                    field_cls = '.'.join(values[0].lower().split('.')[-2:])
                    if field_cls == str(form.fields[field].queryset.
                                        model._meta):
                        url = reverse('arctic:autocomplete', args=[key, ''])
                        choices = ()
                        if form.instance.pk:
                            field_id = getattr(form.instance, field +
                                               '_id')
                            field_value = getattr(form.instance, field)
                            choices = ((field_id, field_value),)
                        form.fields[field].widget = SelectizeAutoComplete(
                            attrs=form.fields[field].widget.attrs,
                            choices=choices,
                            url=url)

            if self.readonly_fields and field in self.readonly_fields:
                form.fields[field].widget.attrs['readonly'] = True
        return form

    def get_form(self, form_class=None):
        form = super(FormMixin, self).get_form(form_class=None)
        try:
            form = self.update_form_fields(form)
        except AttributeError:
            pass
        return form

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
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


class ListMixin(object):
    template_name = 'arctic/base_list.html'
    fields = None  # Which fields should be shown in listing
    ordering_fields = []  # Fields with ordering (subset of fields)
    field_links = {}
    field_classes = {}
    action_links = []  # "Action" links on item level. For example "Edit"
    tool_links = []   # Global links. For Example "Add object"
    default_ordering = []  # Default ordering, e.g. ['title', '-brand']
    search_fields = []
    # Simple search form if search_fields is defined
    simple_search_form_class = SimpleSearchForm
    advanced_search_form_class = None  # Custom form for advanced search
    _simple_search_form = None
    _advanced_search_form = None
    tool_links_icon = 'fa-wrench'
    max_embeded_list_items = 10  # when displaying a list in a column
    primary_key = 'pk'
    sorting_field = None
    sorting_url = None

    @property
    def simple_search_form(self):
        return self._simple_search_form

    @property
    def advanced_search_form(self):
        return self._advanced_search_form

    def ordering_url(self, field_name):
        """
        Creates a url link for sorting the given field.

        The direction of sorting will be either ascending, if the field is not
        yet sorted, or the opposite of the current sorting if sorted.
        """
        path = self.request.path
        direction = ''
        query_params = self.request.GET.copy()
        ordering = self.request.GET.get('order', '').split(',')
        field = self._get_ordering_field_lookup(field_name)
        if not ordering:
            ordering = self.get_default_ordering()
        merged_ordering = list(ordering)  # copy the list

        for ordering_field in self.get_ordering_fields_lookups():
            if (ordering_field.lstrip('-') not in ordering) and \
               (('-' + ordering_field.lstrip('-')) not in ordering):
                merged_ordering.append(ordering_field)

        new_ordering = []
        for item in merged_ordering:
            if item.lstrip('-') == field.lstrip('-'):
                if (item[0] == '-') or not (item in ordering):
                    if item in ordering:
                        direction = 'desc'
                    new_ordering.insert(0, item.lstrip('-'))
                else:
                    direction = 'asc'
                    new_ordering.insert(0, '-' + item)

        query_params['order'] = ','.join(new_ordering)

        return (path + '?' + query_params.urlencode(safe=','), direction)

    def get_fields(self, strip_labels=False):
        """
        Hook to dynamically change the fields that will be displayed
        """
        if strip_labels:
            return [f[0] if type(f) in (tuple, list) else f
                    for f in self.fields]
        return self.fields

    def get_ordering_fields(self):
        """
        Hook to dynamically change the fields that can be ordered
        """
        return self.ordering_fields

    def get_ordering_fields_lookups(self):
        """
        Getting real model fields to order by
        """
        ordering_field = []
        for field_name in self.get_ordering_fields():
            ordering_field.append(self._get_ordering_field_lookup(field_name))
        return ordering_field

    def _get_ordering_field_lookup(self, field_name):
        """
        get real model field to order by
        """
        field = field_name
        get_field = getattr(self, 'get_%s_ordering_field' % field_name, None)
        if get_field:
            field = get_field()
        return field

    def get_tool_links_icon(self):
        return self.tool_links_icon

    def get_search_fields(self):
        """
        Hook to dynamically change the fields that can be searched
        """
        return self.search_fields

    def get_field_links(self):
        if not self.field_links:
            return {}
        else:
            allowed_field_links = {}
            for field, url in self.field_links.items():
                # check permission based on named_url
                if not view_from_url(url).has_permission(self.request.user):
                    continue
                allowed_field_links[field] = url
            return allowed_field_links

    def get_field_classes(self, obj):
        field_classes = self.field_classes
        for field_name in field_classes.keys():
            get_field_name_classes = getattr(
                self, 'get_%s_field_classes' % field_name, None
            )
            if get_field_name_classes:
                field_classes[field_name] = get_field_name_classes(obj)
        return field_classes

    def get_confirm_link(self, url, obj):
        """
        Returns the metadata for a link that needs to be confirmed, if it
        exists, it also parses the message and title of the url to include
        row field data if needed.
        """
        try:
            if type(obj) != dict:
                obj = vars(obj)
            link = {key: value.replace('"', '&quot;') for (key, value) in
                    self.confirm_links[url].items()}
            link['message'] = Template(link['message']).render(Context(obj))
            link['title'] = Template(link['title']).render(Context(obj))
            link['ok']  # this triggers a KeyError exception if not existent
            link['cancel']
            return link
        except KeyError as e:
            raise ImproperlyConfigured(
                'confirm_links requires a dictionary with \'message\', '
                '\'title\', \'ok\' and \'cancel\' strings, the named url \'' +
                url + '\' misses ' + str(e))
        except AttributeError:
            return None

    def _get_field_actions(self, obj):
        all_actions = self.get_action_links()
        get_field_actions = getattr(self, 'get_field_actions', None)
        if get_field_actions:
            field_actions = get_field_actions(obj)
            allowed_field_actions = self._get_allowed_field_actions(
                field_actions,
                all_actions
            )
        else:
            allowed_field_actions = all_actions
        if allowed_field_actions:
            actions = []
            for field_action in allowed_field_actions:
                actions.append({'label': field_action['label'],
                                'icon': field_action['icon'],
                                'url': self._reverse_field_link(
                                    field_action['url'], obj),
                                'confirm': self.get_confirm_link(
                                    field_action['url'], obj),
                                })
            return {'type': 'actions', 'actions': actions}

    def _get_allowed_field_actions(self, field_actions, all_actions):
        allowed_urls = [a['url'] for a in all_actions]
        allowed_actions = []
        for action in field_actions:
            if action[1] in allowed_urls:
                allowed_actions.append(self._build_action_link(action))
        return allowed_actions

    def get_action_links(self):
        self._allowed_action_links = []
        if self.action_links:
            for link in self.action_links:
                url = named_url = link[1]
                if type(url) in (list, tuple):
                    named_url = url[0]
                # check permission based on named_url
                if not view_from_url(named_url).\
                        has_permission(self.request.user):
                    continue
                self._allowed_action_links.append(
                    self._build_action_link(link)
                )
        return self._allowed_action_links

    def _build_action_link(self, action_link):
        icon = action_link[2] if len(action_link) == 3 else None
        return {'label': action_link[0],
                'url': action_link[1],
                'icon': icon}

    def get_tool_links(self):
        if not self.tool_links:
            return []
        else:
            allowed_tool_links = []
            for link in self.tool_links:

                # check permission based on named_url
                if not view_from_url(link[1]).\
                        has_permission(self.request.user):
                    continue

                icon = None
                if len(link) == 3:  # if an icon class is given
                    icon = link[2]
                allowed_tool_links.append({'label': link[0],
                                           'url': link[1],
                                           'icon': icon})
            return allowed_tool_links

    def get_simple_search_form_class(self):
        """
        Hook to dynamically change the simple search form
        """
        if not self.simple_search_form_class and self.get_search_fields():
            return SimpleSearchForm
        return self.simple_search_form_class

    def get_advanced_search_form_class(self):
        """
        Hook to dynamically change the advanced search form
        """
        return self.advanced_search_form_class

    def get_simple_search_form(self, data):
        if self.get_search_fields():
            self._simple_search_form = self.get_simple_search_form_class()(
                search_fields=self.get_search_fields(),
                data=data
            )
        else:
            self._simple_search_form = self.get_simple_search_form_class()(
                data=data)
        return self._simple_search_form

    def get_advanced_search_form(self, data):
        """
        Hook to dynamically change the advanced search form
        """
        if self.get_advanced_search_form_class():
            self._advanced_search_form = self.get_advanced_search_form_class()(
                data=data)
            return self._advanced_search_form


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
        if not user.is_authenticated:
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
