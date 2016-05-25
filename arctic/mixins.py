# -*-*- encoding: utf-8 -*-*-
"""
Basic mixins for generic class based views.
"""
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse

from .utils import menu


class ViewMixin(object):
    """
    Mixin can be used if it is not possible to use one of the generic view classes.
    """
    page_title = ''
    page_description = ''
    sections = []

    def get_context_data(self, **kwargs):
        context = super(ViewMixin, self).get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        context['page_description'] = self.get_page_description()
        context['menu'] = menu(user=self.request.user, request=self.request)
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['sections'] = self.get_sections()
        context['index_url'] = self.get_index_url()
        context['SITE_NAME'] = self.get_site_name()
        context['SITE_LOGO'] = self.get_site_logo()
        return context

    def get_breadcrumbs(self):
        breadcrumbs = []
        return breadcrumbs

    def get_sections(self):
        return self.sections

    def get_page_title(self):
        return self.page_title

    def get_page_description(self):
        return self.page_description

    def get_site_logo(self):
        return getattr(settings, 'ARCTIC_SITE_LOGO', 'arctic/build/images/logo.png')

    def get_site_name(self):
        return getattr(settings, 'ARCTIC_SITE_NAME', 'Arctic Site Name')

    def get_index_url(self):
        try:
            return reverse('index')
        except NoReverseMatch:
            return '/'


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
    Adding links to view, to be resolved with 'dashboard_url' template tag
    """
    def get_links(self):
        if not self.links:
            return None
        else:
            allowed_links = []
            for link in self.links:
                # Lets check permissions
                # if check_url_access(self.request.user, link[1],
                #                     self.get_parent_ids()):
                allowed_links.append(link)
            return allowed_links
