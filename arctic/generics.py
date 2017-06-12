from __future__ import (division, unicode_literals)

from collections import OrderedDict

import extra_views
from django.conf import settings
from django.contrib.auth import (authenticate, login, logout)
from django.core.exceptions import (FieldDoesNotExist, ImproperlyConfigured)
from django.core.urlresolvers import (NoReverseMatch, reverse)
from django.db.models.deletion import (Collector, ProtectedError)
from django.forms.widgets import Media
from django.shortcuts import (redirect, render, resolve_url)
from django.utils.formats import get_format
from django.utils.http import is_safe_url, quote
from django.utils.text import capfirst
from django.utils.translation import (get_language, ugettext as _)
from django.views import generic as base

from arctic.mixins import FormMediaMixin
from .filters import filterset_factory
from .mixins import (LinksMixin, RoleAuthentication, SuccessMessageMixin,
                     LayoutMixin)
from .utils import (find_attribute, get_field_class, find_field_meta,
                    get_attribute, menu, view_from_url)


class View(RoleAuthentication, base.View):
    """
    This view needs to be used for all Arctic views, except the LoginView.

    It includes integration with the Arctic user interface elements, such as
    the menu, site logo, site title, page title and breadcrumbs.
    """

    page_title = ''
    page_description = ''
    breadcrumbs = None
    tabs = None
    requires_login = True
    urls = {}

    def dispatch(self, request, *args, **kwargs):
        """
        Most views in a CMS require a login, so this is the default setup.

        If a login is not required then the requires_login property
        can be set to False to disable this.
        """
        if self.requires_login:
            if settings.LOGIN_URL is None or settings.LOGOUT_URL is None:
                raise ImproperlyConfigured(
                    'LOGIN_URL and LOGOUT_URL '
                    'has to be defined if requires_login is True'
                )

            if not request.user.is_authenticated():
                return redirect('%s?next=%s' % (
                    resolve_url(settings.LOGIN_URL),
                    quote(request.get_full_path())))

        return super(View, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        context['page_description'] = self.get_page_description()
        context['menu'] = menu(user=self.request.user, request=self.request)
        context['urls'] = self.get_urls()
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['tabs'] = self.get_tabs()
        context['index_url'] = self.get_index_url()
        context['SITE_NAME'] = self.get_site_name()
        context['SITE_TITLE'] = self.get_site_title()
        context['SITE_LOGO'] = self.get_site_logo()
        context['TOPBAR_BACKGROUND_COLOR'] = self.get_topbar_background_color()
        context['HIGHLIGHT_COLOR'] = self.get_highlight_color()
        context['DATETIME_FORMATS'] = self.get_datetime_formats()
        context['LOGIN_URL'] = self.get_login_url()
        context['LOGOUT_URL'] = self.get_logout_url()
        context['media'] = self.media
        return context

    def get_urls(self):
        """
        Used for resolving urls when displaying nested objects, see arctic_url.

        For example, generally you just have /foo/create as
        a url, but with nested, you may have: /foo/<id>/bar/create/ and <id>
        would be a parent id. These are then required to resolve urls.

        @returns
        {named_url, (url_param, url_param),}
        || {named_url, [url_param, url_param],}

        if you provide a list and in this list there are strings, it will try
        to get field of that item. This is especially useful for listviews with
        action_links and field_links.
        """
        return self.urls

    def get_breadcrumbs(self):
        """
        Breadcrumb format: (('name', 'url'), ...) or None if not used.
        """
        if not self.breadcrumbs:
            return None
        else:
            allowed_breadcrumbs = []
            for breadcrumb in self.breadcrumbs:

                # check permission based on named_url
                if breadcrumb[1] is not None \
                        and not view_from_url(
                            breadcrumb[1]).has_permission(self.request.user):
                    continue

                allowed_breadcrumbs.append(breadcrumb)
            return allowed_breadcrumbs

    def get_tabs(self):
        """
        Tabs format: (('name', 'url'), ...) or None if tabs are not used.
        """
        if not self.tabs:
            return None
        else:
            allowed_tabs = []
            for tab in self.tabs:

                # check permission based on named_url
                if not view_from_url(tab[1]).has_permission(self.request.user):
                    continue

                allowed_tabs.append(tab)
            return allowed_tabs

    def get_page_title(self):
        return self.page_title

    def get_page_description(self):
        return self.page_description

    def get_site_logo(self):
        return getattr(settings, 'ARCTIC_SITE_LOGO',
                       'arctic/dist/assets/img/arctic_logo.svg')

    def get_site_name(self):
        return getattr(settings, 'ARCTIC_SITE_NAME',
                       'Arctic Site Name')

    def get_site_title(self):
        return getattr(settings, 'ARCTIC_SITE_TITLE',
                       self.get_site_name())

    def get_topbar_background_color(self):
        return getattr(settings, 'ARCTIC_TOPBAR_BACKGROUND_COLOR', None)

    def get_highlight_color(self):
        return getattr(settings, 'ARCTIC_HIGHLIGHT_COLOR', None)

    def get_index_url(self):
        try:
            return reverse(getattr(settings, 'ARCTIC_INDEX_URL', 'index'))
        except NoReverseMatch:
            return '/'

    def get_datetime_formats(self):
        dtformats = {}

        dtformats['SHORT_DATE'] = get_format('DATE_INPUT_FORMATS',
                                             get_language())[0]
        dtformats['TIME'] = get_format('TIME_INPUT_FORMATS',
                                       get_language())[0]
        dtformats['SHORT_DATETIME'] = get_format('DATETIME_INPUT_FORMATS',
                                                 get_language())[0]

        return dtformats

    def get_login_url(self):
        login_url = getattr(settings, 'LOGIN_URL', 'login')
        return reverse(login_url) if login_url else None

    def get_logout_url(self):
        logout_url = getattr(settings, 'LOGOUT_URL', 'logout')
        return reverse(logout_url) if logout_url else None

    @property
    def media(self):
        """
        Return all media required to render this view, including forms.
        """
        media = self._get_common_media()
        media += self._get_view_media()
        media += self.get_media_assets()
        return media

    def _get_common_media(self):
        config = getattr(settings, 'ARCTIC_COMMON_MEDIA_ASSETS', [])
        media = Media()
        if 'css' in config:
            media.add_css(config['css'])
        if 'js' in config:
            media.add_js(config['js'])
        return media

    def get_media_assets(self):
        """
        Allows to define additional media for view
        """
        return Media()

    def _get_view_media(self):
        """
        Gather view-level media assets
        """
        media = Media()
        try:
            media.add_css(self.Media.css)
        except AttributeError:
            pass
        try:
            media.add_js(self.Media.js)
        except AttributeError:
            pass
        return media


class TemplateView(View, base.TemplateView):
    pass


class DetailView(View, LinksMixin, base.DetailView):
    """
    Custom detail view.
    """

    fields = None            # Which fields should be shown in the details
    links = None             # Optional links such as list of linked items

    def get_fields(self, obj):
        result = OrderedDict()
        if self.fields:
            for field_name in self.fields:
                if isinstance(field_name, tuple):
                    # custom property that is not a field of the model
                    result[field_name[1]] = getattr(obj, field_name[0])
                else:
                    field = self.model._meta.get_field(field_name)
                    result[field.verbose_name.title()] = getattr(obj,
                                                                 field_name)
        return result

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['fields'] = self.get_fields(context['object'])
        context['links'] = self.get_links()
        return context


class ListView(View, base.ListView):
    """
    Custom listview. Adding filter, sorting and display logic.
    """
    template_name = 'arctic/base_list.html'
    fields = None  # Which fields should be shown in listing
    filter_fields = []  # One on one maping to django-filter fields meta option
    search_fields = []
    ordering_fields = []  # Fields with ordering (subset of fields)
    default_ordering = []  # Default ordering, e.g. ['title', '-brand']
    action_links = []  # "Action" links on item level. For example "Edit"
    field_links = {}
    field_classes = {}
    tool_links_icon = 'fa-wrench'
    tool_links = []   # Global links. For Example "Add object"
    prefix = ''  # Prefix for embedding multiple list views in detail view
    max_embeded_list_items = 10  # when displaying a list in a column
    primary_key = 'pk'

    def get(self, request, *args, **kwargs):
        objects = self.get_object_list()
        context = self.get_context_data(object_list=objects)

        return self.render_to_response(context)

    def get_object_list(self):
        if self.get_filter_fields() or self.get_search_fields():
            filterset_class = self.get_filterset_class()
            self.filterset = self.get_filterset(filterset_class)
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.get_queryset()

        return self.object_list

    def ordering_url(self, field):
        """
        Creates a url link for sorting the given field.

        The direction of sorting will be either ascending, if the field is not
        yet sorted, or the opposite of the current sorting if sorted.
        """
        path = self.request.path
        direction = ''
        query_params = self.request.GET.copy()
        ordering = self.request.GET.get('order', '').split(',')
        if not ordering:
            ordering = self.get_default_ordering()
        merged_ordering = list(ordering)  # copy the list

        for ordering_field in self.get_ordering_fields():
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

    def get_fields(self):
        """
        Hook to dynamically change the fields that will be displayed
        """
        return self.fields

    def get_ordering_fields(self):
        """
        Hook to dynamically change the fields that can be ordered
        """
        return self.ordering_fields

    def get_filter_fields(self):
        """
        Hook to dynamically change the fields that can be filtered
        """
        return self.filter_fields

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

    def _reverse_field_link(self, url, obj):
        if type(url) in (list, tuple):
            named_url = url[0]
            args = []
            for arg in url[1:]:
                args.append(find_attribute(obj, arg))
        else:
            named_url = url
            args = [get_attribute(obj, self.primary_key)]

        # Instead of giving NoReverseMatch exception
        # its more desirable, for field_links in listviews
        # to just ignore the link.
        if None in args:
            return ""

        return reverse(named_url, args=args)

    def get_field_classes(self):
        return self.field_classes

    def get_list_header(self):
        """
        Creates a list of dictionaries with the field names, labels,
        field links, field css classes, order_url and order_direction,
        this simplifies the creation of a table in a template.
        """
        model = self.object_list.model
        result = []
        if not self.get_fields():
            result.append({
                'name': '',
                'verbose': str(model._meta.verbose_name),
            })
        else:
            prefix = self.get_prefix()
            for field_name in self.get_fields():
                item = {}
                if isinstance(field_name, tuple):
                    # custom property that is not a field of the model
                    name = field_name[0]
                    item['label'] = field_name[1]
                else:
                    name = field_name
                    try:
                        field_meta = find_field_meta(
                            model,
                            field_name
                        )
                        if field_meta._verbose_name:  # noqa
                            # explicitly set on the model, so don't change
                            item['label'] = field_meta._verbose_name  # noqa
                        else:
                            # title-case the field name (issue #80)
                            item['label'] = field_meta.verbose_name.title()

                        # item['label'] = model._meta.get_field(field_name).\
                        #     verbose_name
                    except FieldDoesNotExist:
                        item['label'] = field_name
                    except AttributeError:
                        item['label'] = field_name
                item['name'] = prefix + name
                if name in self.get_ordering_fields():
                    item['order_url'], item['order_direction'] = \
                        self.ordering_url(name)
                result.append(item)

        return result

    def get_list_items(self, objects):
        self.has_action_links = False
        items = []
        if not self.get_fields():
            for obj in objects:
                items.append([obj.pk, str(obj)])
            return items

        # remove all tuples in the field list, no need for the verbose
        # field name here
        fields = []
        field_links = self.get_field_links()
        field_classes = self.get_field_classes()
        field_actions = self.get_action_links()
        for field in self.get_fields():
            fields.append(field[0] if type(field) in (list, tuple)
                          else field)
        for obj in objects:
            row = []

            for field_name in fields:
                field = {'type': 'field', 'field': field_name}
                base_field_name = field_name.split('__')[0]
                field_class = get_field_class(objects, base_field_name)
                field['value'] = self.get_field_value(field_name, obj)
                if field_class == 'ManyToManyField':
                    #  ManyToManyField will be display as an embedded list
                    #  capped to max_embeded_list_items, an ellipsis is
                    #  added if there are more items than the max.
                    m2mfield = getattr(obj, base_field_name)
                    embeded_list = list(str(l) for l in
                                        m2mfield.all()
                                        [:self.max_embeded_list_items + 1])
                    if len(embeded_list) > self.max_embeded_list_items:
                        embeded_list = embeded_list[:-1] + ['...']
                    field['value'] = embeded_list
                if field_name in field_links.keys():
                    field['url'] = self._reverse_field_link(
                        field_links[field_name], obj)
                if field_name in field_classes:
                    field['class'] = field_classes[field_name]
                row.append(field)
            if field_actions:
                actions = []
                for field_action in field_actions:
                    actions.append({'label': field_action['label'],
                                    'icon': field_action['icon'],
                                    'url': self._reverse_field_link(
                                        field_action['url'], obj)})
                row.append({'type': 'actions', 'actions': actions})
                self.has_action_links = True
            items.append(row)

            print(items)
        return items

    def get_field_value(self, field_name, obj):
        try:  # first try to find a virtual field
            virtual_field_name = "get_{}_field".format(field_name)
            return getattr(self, virtual_field_name)(obj)
        except AttributeError:  # then try get_{field}_display
            try:
                # Get the choice display value
                parent_objs = '__'.join(
                    field_name.split('__')[:-1])
                method_name = '{}__get_{}_display'.format(
                    parent_objs,
                    field_name.split('__')[-1]).strip('__')
                return find_attribute(obj, method_name)()
            except (AttributeError, TypeError):
                # finally get field's value
                return find_attribute(obj, field_name)

    def get_action_links(self):
        if not self.action_links:
            return []
        else:
            allowed_action_links = []
            for link in self.action_links:
                url = named_url = link[1]
                if type(url) in (list, tuple):
                    named_url = url[0]
                # check permission based on named_url
                if not view_from_url(named_url).\
                        has_permission(self.request.user):
                    continue

                icon = None
                if len(link) == 3:  # if an icon class is given
                    icon = link[2]
                allowed_action_links.append({'label': link[0],
                                             'url': url,
                                             'icon': icon})
            return allowed_action_links

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

    def get_tool_links_icon(self):
        return self.tool_links_icon

    def get_prefix(self):
        return self.prefix + '-' if self.prefix else ''

    def get_default_ordering(self):
        prefix = self.get_prefix()
        return [prefix + f for f in self.default_ordering]

    def get_ordering_with_prefix(self):
        return self.request.GET.getlist('order', self.get_default_ordering())

    def get_ordering(self):
        """Ordering used for queryset filtering (should not contain prefix)."""
        prefix = self.get_prefix()
        fields = self.get_ordering_with_prefix()
        if self.prefix:
            fields = [f.replace(prefix, '', 1) for f in fields]
        return [f for f in fields if f.lstrip('-')
                in self.get_ordering_fields()]

    def get_filterset_class(self):
        if not self.get_filter_fields() and not self.get_search_fields():
            return None

        return filterset_factory(
            model=self.model or self.queryset.model,
            fields=self.get_filter_fields(),
            search_fields=self.get_search_fields()
        )

    def get_filterset(self, filterset_class):
        """
        Returns an instance of the filterset to be used in this view.
        """
        kwargs = self.get_filterset_kwargs(filterset_class)
        return filterset_class(**kwargs)

    def get_filterset_kwargs(self, filterset_class):
        """
        Returns the keyword arguments for instantiating the filterset.
        """
        data = self.request.GET.copy()
        for key in self.request.GET:
            if not data[key]:
                data.pop(key)

        kwargs = {
            'data': data,
            'queryset': self.get_queryset(),
        }
        if self.prefix:
            kwargs['prefix'] = self.prefix
        return kwargs

    def get_page_title(self):
        if not self.page_title:
            return capfirst(self.object_list.model._meta.verbose_name_plural)
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['prefix'] = self.prefix
        context['list_header'] = self.get_list_header()
        context['list_items'] = self.get_list_items(context['object_list'])
        context['tool_links'] = self.get_tool_links()
        # self.has_action_links is set in get_list_items
        context['has_action_links'] = self.has_action_links
        context['tool_links_icon'] = self.get_tool_links_icon()
        if self.get_filter_fields() or self.get_search_fields():
            context['has_filter'] = True
            context['filter'] = self.filterset
        return context


class CreateView(FormMediaMixin, View, SuccessMessageMixin,
                 LayoutMixin, extra_views.CreateWithInlinesView):
    template_name = 'arctic/base_create_update.html'
    success_message = _('%(object)s was created successfully')

    def get_page_title(self):
        if not self.page_title:
            return _("Create %s") % self.model._meta.verbose_name
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['layout'] = self.get_layout()
        return context


class UpdateView(FormMediaMixin, SuccessMessageMixin, LayoutMixin, View,
                 LinksMixin, extra_views.UpdateWithInlinesView):
    template_name = 'arctic/base_create_update.html'
    success_message = _('%(object)s was updated successfully')

    links = None             # Optional links such as list of linked items
    readonly_fields = None   # Optional list of readonly fields

    def get_page_title(self):
        if not self.page_title:
            return _("Edit %s") % self.model._meta.verbose_name
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['links'] = self.get_links()
        context['layout'] = self.get_layout()
        return context


class FormView(FormMediaMixin, View, SuccessMessageMixin, LayoutMixin,
               base.FormView):
    template_name = 'arctic/base_create_update.html'


class DeleteView(SuccessMessageMixin, View, base.DeleteView):
    template_name = 'arctic/base_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        """
        Catch protected relations and show to user.
        """
        self.object = self.get_object()
        can_delete = True
        protected_objects = []
        collector_message = None
        collector = Collector(using='default')
        try:
            collector.collect([self.object])
        except ProtectedError as e:
            collector_message = "Cannot delete %s because it has relations " \
                                "that depends on it." % self.object
            protected_objects = e.protected_objects
            can_delete = False

        context = self.get_context_data(object=self.object,
                                        can_delete=can_delete,
                                        collector_message=collector_message,
                                        protected_objects=protected_objects)
        return self.render_to_response(context)


class LoginView(TemplateView):
    template_name = 'arctic/login.html'
    page_title = 'Login'
    requires_login = False

    def __init__(self, *args, **kwargs):
        super(TemplateView, self).__init__(*args, **kwargs)
        # thread-safe definition of messages.
        self.messages = []

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LoginView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')
        context['username'] = self.request.POST.get('username', '')
        context['messages'] = set(self.messages)
        return context

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user and user.is_active:
            login(request, user)

            next_url = request.GET.get('next')
            if is_safe_url(next_url, request.get_host()):
                return redirect(next_url)

            return redirect('/')

        self.messages.append('Invalid username/password combination')

        return render(request, self.template_name,
                      self.get_context_data(**kwargs))
