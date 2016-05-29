# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy, reverse

from arctic.generics import (
    ListView, UpdateView, CreateView,
    DeleteView, TemplateView)

from .models import Article, Category
from .forms import ArticleForm
from .inlines import ArticleInline, TagsInline


class DashboardView(TemplateView):
    template_name = 'arctic/index.html'
    page_title = "Dashboard"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class ArticleListView(ListView):
    paginate_by = 20
    model = Article
    fields = ['title', 'description', 'published', 'category']
    ordering_fields = ['title', 'description', 'published']
    search_fields = ['title']
    action_links = [
        ('delete', 'articles:delete'),
    ]
    field_links = {
        'title': 'articles:detail',
        'published': 'articles:detail',
    }
    field_classes = {
        'published': 'inline-widget boolean-circle',
    }
    tool_links = [
        (_('Add Article'), 'articles:create'),
    ]
    paginate_by = 2


class ArticleListViewInline(ArticleListView):
    template_name = 'arctic/partials/base_data_table.html'
    prefix = 'articles'

    def get_object_list_for_parent(self, parent_id):
        return self.get_object_list().filter(category_id=parent_id)


class ArticleDetailView(UpdateView):
    page_title = _("Edit Article")
    model = Article
    success_url = reverse_lazy('articles:list')
    form_class = ArticleForm
    links = [('Back to list', 'articles:list')]
    inlines = [TagsInline]
    # inline_views = [ArticleListViewInline]


class ArticleCreateView(CreateView):
    page_title = _("Create Article")
    model = Article
    fields = ['title', 'description', 'category', 'published']

    def get_success_url(self):
        return reverse('articles:detail', args=(self.object.pk,))


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('articles:list')


class CategoryListView(ListView):
    page_title = _("Categories")
    model = Category
    list_display = ['name']
    column_links = {
        'name': 'articles:category-detail',
    }
    tool_links = [
        (_('Add Category'), 'articles:category-create'),
    ]


class CategoryDetailView(UpdateView):
    page_title = _("Edit Category")
    model = Category
    inlines = [ArticleInline]
    success_url = reverse_lazy('articles:category-list')


class CategoryCreateView(CreateView):
    page_title = _("Create Category")
    model = Category
    fields = ['name']
    def get_success_url(self):
        return reverse('articles:category-detail', args=(self.object.pk,))


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('articles:category-list')