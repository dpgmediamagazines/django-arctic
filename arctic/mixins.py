# -*-*- encoding: utf-8 -*-*-
"""
Basic mixins for generic class based views.
"""

from __future__ import unicode_literals, absolute_import

from django.contrib import messages


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
                # Lets check permissions
                # if check_url_access(self.request.user, link[1],
                #                     self.get_parent_ids()):
                allowed_links.append(link)
            return allowed_links
