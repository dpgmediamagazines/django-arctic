# -*-*- encoding: utf-8 -*-*-
# pylint: disable=E1101,W0201
"""
Generic views that provide commonly needed behaviour.
"""
from __future__ import unicode_literals, division
from collections import OrderedDict

from collections import OrderedDict
from django.views import generic as base
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils.text import capfirst
from django.db.models.deletion import Collector, ProtectedError
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings

import extra_views

from .filters import filterset_factory
from .mixins import SuccessMessageMixin, LinksMixin
from .templatetags.arctic_tags import arctic_url
from .utils import menu


class View(base.View):
    """
    This view needs to be used for all Arctic views, except the LoginView
    It includes integration with the Arctic user interface elements, such as
    the menu, site logo, site title, page title and breadcrumbs.
    """

    page_title = ''
    page_description = ''
    breadcrumbs = None

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        context['page_description'] = self.get_page_description()
        context['menu'] = menu(user=self.request.user, request=self.request)
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['index_url'] = self.get_index_url()
        context['SITE_NAME'] = self.get_site_name()
        context['SITE_LOGO'] = self.get_site_logo()
        return context

    def get_breadcrumbs(self):
        """
        breadcrumb format:
        (('name', 'url'), ...)
        or None if breadcrumbs are not to be used.
        """
        return self.breadcrumbs

    def get_page_title(self):
        return self.page_title

    def get_page_description(self):
        return self.page_description

    def get_site_logo(self):
        return getattr(settings, 'ARCTIC_SITE_LOGO',
                       'arctic/build/images/logo.png')

    def get_site_name(self):
        return getattr(settings, 'ARCTIC_SITE_NAME',
                       'Arctic Site Name')

    def get_site_title(self):
        return getattr(settings, 'ARCTIC_SITE_TITLE',
                       self.get_site_name())

    def get_index_url(self):
        try:
            return reverse('index')
        except NoReverseMatch:
            return '/'


class TemplateView(View, base.TemplateView):
    pass


class DetailView(View, LinksMixin, base.DetailView):
    """
    Custom detail view.
    """

    fields = None  # Which fields should be shown in the details
    links = None   # Optional links such as viewing list of linked items

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
    tool_links = []   # Global links. For Example "Add object"
    prefix = ''  # Prefix for embedding multiple list views in detail view

    def get(self, request, *args, **kwargs):
        objects = self.get_object_list()
        context = self.get_context_data(object_list=objects)

        return self.render_to_response(context)

    def render(self, parent_id):
        """Render to string in context of parent with parent_id."""
        objects = self.get_object_list_for_parent(parent_id)
        context = self.get_context_data(object_list=objects)
        result = render_to_string(self.template_name, context,
                                  request=self.request)
        return result

    def get_object_list(self):
        if self.filter_fields or self.search_fields:
            filterset_class = self.get_filterset_class()
            self.filterset = self.get_filterset(filterset_class)
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.get_queryset()

        return self.object_list

    def get_object_list_for_parent(self, parent_id):
        raise NotImplementedError('Must override for embedded list view')

    def get_parent_ids(self):
        """
        Used for resolving urls when displaying nested objects.
        Generally, you just have /foo/create as a url, but with nexted,
        you may have: /foo/<id>/bar/create/ and <id> would be a parent id.
        These are then required to resolve urls.
        """
        return None

    def ordering_url(self, field):
        """
        Creates a url link for sorting the given field, the direction of
        sorting will be either ascending if the field is not yet sorted, or the
        opposite of the current sorting if the field is sorted.
        """

        path = self.request.path
        direction = ''
        query_params = self.request.GET.copy()
        ordering = self.request.GET.get('order', '').split(',')
        if not ordering:
            ordering = self.get_default_ordering()
        merged_ordering = list(ordering)  # copy the list

        for ordering_field in self.ordering_fields:
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
        return self.fields

    def get_field_links(self):
        return self.field_links

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
                    item['label'] = model._meta.get_field(field_name).\
                        verbose_name
                item['name'] = prefix + name
                if name in self.get_field_links().keys():
                    item['link'] = self.get_field_links()[name]
                if name in self.get_field_classes().keys():
                    item['class'] = self.get_field_classes()[name]
                if name in self.ordering_fields:
                    item['order_url'], item['order_direction'] = \
                        self.ordering_url(name)
                result.append(item)

        return result

    def get_list_items(self, objects):
        items = []
        if not self.fields:
            for obj in objects:
                items.append([obj.pk, str(obj)])
        else:
            for obj in objects:
                item = [obj.pk]
                for field_name in self.fields:
                    if isinstance(field_name, tuple):
                        value = getattr(obj, field_name[0])
                    else:
                        try:
                            # Get the choice display value
                            method_name = 'get_{}_display'.format(field_name)
                            value = getattr(obj, method_name)()
                        except AttributeError:
                            # Get the regular field value
                            value = getattr(obj, field_name)

                    item.append(value)
                items.append(item)

        return items

    def get_action_links(self):
        if not self.action_links:
            return None
        else:
            allowed_action_links = []
            for link in self.action_links:
                # Lets check permissions
                # TODO: Hardcoded pk added as arg list, refactor when we
                # implement object level permissions.
                # NOT sure if we should refactor, it makes more sense to check
                # for object level permissions
                # when gathering the queryset. If we do it while rendering a
                # page, then we work on paginated
                # queryset and we may get uneven sized pages.
                '''
                url_args = (1,)
                parent_ids = self.get_parent_ids()
                if parent_ids:
                    url_args += parent_ids
                if check_url_access(self.request.user, link[1], url_args):
                '''
                allowed_action_links.append(link)
            return allowed_action_links

    def get_tool_links(self):
        if not self.tool_links:
            return None
        else:
            allowed_tool_links = []
            for link in self.tool_links:
                # Lets check permissions
                # if check_url_access(self.request.user, link[1],
                # self.get_parent_ids()):
                allowed_tool_links.append(link)

            return allowed_tool_links

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
        return [f for f in fields if f.lstrip('-') in self.ordering_fields]

    def get_filterset_class(self):
        if not self.filter_fields and not self.search_fields:
            return None

        return filterset_factory(self.model or self.queryset.model,
                                 self.filter_fields, self.search_fields)

    def get_filterset(self, filterset_class):
        """
        Returns an instance of the filterset to be used in this view.
        """
        kwargs = self.get_filterset_kwargs(filterset_class)
        return filterset_class(**kwargs)

    def get_filterset_kwargs(self, filterset_class):
        """
        Returns the keyword arguments for instanciating the filterset.
        """
        kwargs = {
            'data': self.request.GET or None,
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
        context['action_links'] = self.get_action_links()
        context['tool_links'] = self.get_tool_links()
        if self.filter_fields or self.search_fields:
            context['has_filter'] = True
            context['filter'] = self.filterset
        return context


class CreateView(View, SuccessMessageMixin, base.CreateView):
    template_name = 'arctic/base_detail.html'
    success_message = _('%(object)s was created successfully')

    def get_page_title(self):
        if not self.page_title:
            return _("Create %s") % self.model._meta.verbose_name
        return self.page_title


class UpdateWithInlinesView(LinksMixin, extra_views.UpdateWithInlinesView):
    links = None   # Optional links such as viewing list of linked items
    inline_views = []

    def get_parent_ids(self):
        """
        Used for resolving urls when displaying nested objects.
        Generally, you just have /foo/create as a url, but with nested,
        you may have: /foo/<id>/bar/create/ and <id> would be a parent id.
        These are then required to resolve urls.
        """
        return (self.object.id,)

    def get_context_data(self, **kwargs):
        context = super(UpdateWithInlinesView, self).get_context_data(**kwargs)
        context['links'] = self.get_links()
        context['inline_views'] = self.inline_views
        return context


class UpdateView(SuccessMessageMixin, View, UpdateWithInlinesView):
    template_name = 'arctic/base_detail.html'
    success_message = _('%(object)s was updated successfully')

    def get_page_title(self):
        if not self.page_title:
            return _("Edit %s") % self.model._meta.verbose_name
        return self.page_title


class DeleteView(SuccessMessageMixin, View, base.DeleteView):
    template_name = 'arctic/base_confirm_detail.html'

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
