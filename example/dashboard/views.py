# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy, reverse

# TODO: Move extra views into our own views. So we can override where needed
from extra_views import InlineFormSet

from arctic.generics import (
    ListView, UpdateView, CreateView,
    DeleteView, TemplateView)


class DashboardView(TemplateView):
    template_name = 'arctic/index.html'
    page_title = "Dashboard"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context

