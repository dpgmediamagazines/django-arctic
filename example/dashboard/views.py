# -*-*- encoding: utf-8 -*-*-
from __future__ import absolute_import, unicode_literals

from arctic.generics import TemplateView


class DashboardView(TemplateView):
    template_name = "arctic/index.html"
    page_title = "Dashboard"
    requires_login = False

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context
