# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy, reverse

# TODO: Move extra views into our own views. So we can override where needed
from extra_views import InlineFormSet

from arctic.generics import (
    ListView, UpdateView, CreateView,
    DeleteView, TemplateView)

from .models import Article
from .forms import ArticleForm


class DashboardView(TemplateView):
    template_name = 'arctic/index.html'
    page_title = "Dashboard"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class ArticleListView(ListView):
    paginate_by = 20
    model = Article
    list_filter = []
    search_fields = ['title']
    list_display = ['title', 'description']
    list_display_links = [
        ('delete', 'articles:delete'),
    ]
    column_links = {
        'title': 'articles:detail',
    }
    column_widgets = {
        'title': 'widget-test',
    }
    tool_links = [
        (_('Add Article'), 'articles:create'),
    ]


class ArticleDetailView(UpdateView):
    page_title = _("Edit Article")
    model = Article
    success_url = reverse_lazy('articles:list')
    form_class = ArticleForm


class ArticleCreateView(CreateView):
    page_title = _("Create Article")
    model = Article
    fields = ['title', 'description']

    def get_success_url(self):
        return reverse('articles:detail', args=(self.object.pk,))


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('articles:list')
