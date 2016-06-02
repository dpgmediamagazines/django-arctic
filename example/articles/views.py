# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy, reverse

from arctic.generics import (
    ListView, UpdateView, CreateView,
    DeleteView, TemplateView)

from .models import Article, Category, Tag
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
    breadcrumbs = (('Home', 'index'), ('Article List', None))
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


class ArticleDetailTagsView(UpdateView):
    page_title = _("Edit Article: Tags")
    model = Article
    inlines = [TagsInline]
    fields = []
    success_url = reverse_lazy('articles:list')

    tabs = [
        ('Detail', 'articles:detail'),
        ('Tags', 'articles:detail-tags'),
    ]

    def get_urls(self):
        return {
            'articles:detail': (self.object.pk,),
            'articles:detail-tags': (self.object.pk,),
        }


class ArticleDetailView(UpdateView):
    page_title = _("Edit Article")
    model = Article
    success_url = reverse_lazy('articles:list')
    form_class = ArticleForm
    links = [
        ('Back to list', 'articles:list'),
        ('Goto main category', 'articles:category-detail'),
    ]
    tabs = [
        ('Detail', 'articles:detail'),
        ('Tags', 'articles:detail-tags'),
    ]

    def get_urls(self):
        return {
            'articles:list': (),
            'articles:detail': (self.object.pk,),
            'articles:category-detail': (self.object.category.pk,),
            'articles:detail-tags': (self.object.pk,),
        }


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
    fields = ['name']
    field_links = {
        'name': 'articles:category-detail',
    }
    tool_links = [
        (_('Add Category'), 'articles:category-create'),
    ]


class CategoryArticlesListView(ArticleListView):

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        return super(CategoryArticlesListView, self).dispatch(request, *args, **kwargs)

    # disable some settings from the default article list
    tool_links = [
    ]
    page_title = "Edit Category: Articles"
    breadcrumbs = None

    tabs = [
        ('Detail', 'articles:category-detail'),
        ('Articles', 'articles:category-articles-list'),
    ]

    def get_urls(self):
        return {
            'articles:category-detail': (self.pk,),
            'articles:category-articles-list': (self.pk,),
        }

    def get_queryset(self):
        qs = super(CategoryArticlesListView, self).get_queryset()
        return qs.filter(category_id=self.pk)


class CategoryDetailView(UpdateView):
    page_title = _("Edit Category")
    model = Category
    success_url = reverse_lazy('articles:category-list')
    tabs = [
        ('Detail', 'articles:category-detail'),
        ('Articles', 'articles:category-articles-list'),
    ]

    def get_urls(self):
        return {
            'articles:category-detail': (self.object.pk,),
            'articles:category-articles-list': (self.object.pk,),
        }


class CategoryCreateView(CreateView):
    page_title = _("Create Category")
    model = Category
    fields = ['name']
    def get_success_url(self):
        return reverse('articles:category-detail', args=(self.object.pk,))


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('articles:category-list')