from __future__ import (absolute_import, unicode_literals)

from django.core.urlresolvers import (reverse, reverse_lazy)
from django.utils.translation import ugettext as _

from arctic.generics import (CreateView, DeleteView, ListView, TemplateView,
                             UpdateView)
from collections import OrderedDict

from .forms import ArticleForm
from .inlines import TagsInline
from .models import (Article, Category, Tag)


class DashboardView(TemplateView):
    template_name = 'arctic/index.html'
    page_title = "Dashboard"
    permission_required = 'view_dashboard'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class ArticleListView(ListView):
    template_name = 'arctic/article_list.html'
    paginate_by = 2
    model = Article
    fields = ['title', 'description', 'published', 'category', 'tags']
    ordering_fields = ['title', 'description', 'published']
    search_fields = ['title']
    breadcrumbs = (('Home', 'index'), ('Article List', None))
    action_links = [
        ('delete', 'articles:delete', 'fa-trash'),
    ]
    field_links = {
        'title': 'articles:detail',
        'published': 'articles:detail',
        'category': ('articles:category-detail', 'category_id'),
    }
    field_classes = {
        'published': 'inline-widgetboolean-circle',
    }
    tool_links = [
        (_('Create Article'), 'articles:create', 'fa-plus'),
    ]

    filter_fields = ['published']
    permission_required = "view_article"

    def get_category_field(self, row):
        return row.category.name


class ArticleUpdateView(UpdateView):
    page_title = _("Edit Article")
    permission_required = "change_article"
    model = Article
    success_url = reverse_lazy('articles:list')
    inlines = [TagsInline]
    form_class = ArticleForm
    links = [
        ('Back to list', 'articles:list'),
    ]
    layout = OrderedDict([
                        ('',
                         ['title|10', ['category', 'tags|5']]),
                        ('Body|Extra Information for this fieldset',
                         ['description']),
                        ('Extended Details',
                         [['published|4', 'updated_at']])])
    # layout = ['title|3', 'title', 'title', ['category', 'category']]

    # tabs = [
    #     ('Detail', 'articles:detail'),
    #     ('Tags', 'articles:detail-tags'),
    # ]

    def get_urls(self):
        return {
            'articles:list': (),
            'articles:detail': (self.object.pk,),
            'articles:category-detail': (self.object.category.pk,),
            'articles:detail-tags': (self.object.pk,),
        }


class ArticleCreateView(CreateView):
    page_title = _("Create Article")
    # fields = ['title', 'description', 'tags', 'category', 'published']
    model = Article
    form_class = ArticleForm
    permission_required = "add_article"
    layout = OrderedDict([
                        ('-Basic Details',
                         ['title|10', ['category', 'tags|5']]),
                        ('Body|Extra Information for this fieldset',
                         ['description']),
                        ('Extended Details',
                         [['published|4', 'updated_at']])])

    def get_success_url(self):
        return reverse('articles:detail', args=(self.object.pk,))


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('articles:list')
    permission_required = "delete_article"


class CategoryListView(ListView):
    page_title = _("Categories")
    model = Category
    fields = ['name']
    field_links = {
        'name': 'articles:category-detail',
    }
    tool_links = [
        (_('Create Category'), 'articles:category-create'),
    ]
    permission_required = 'view_category'


class CategoryArticlesListView(ArticleListView):

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        return super(CategoryArticlesListView, self).dispatch(request, *args,
                                                              **kwargs)

    # disable some settings from the default article list
    tool_links = [
    ]
    page_title = "Edit Category: Articles"
    breadcrumbs = None

    tabs = [
        ('Detail', 'articles:category-detail'),
        ('Related Articles', 'articles:category-articles-list'),
    ]
    permission_required = 'view_category'

    def get_urls(self):
        return {
            'articles:category-detail': (self.pk,),
            'articles:category-articles-list': (self.pk,),
        }

    def get_queryset(self):
        qs = super(CategoryArticlesListView, self).get_queryset()
        return qs.filter(category_id=self.pk)


class CategoryUpdateView(UpdateView):
    page_title = _("Edit Category")
    model = Category
    success_url = reverse_lazy('articles:category-list')
    tabs = [
        ('Detail', 'articles:category-detail'),
        ('Related Articles', 'articles:category-articles-list'),
    ]
    permission_required = 'change_category'

    def get_urls(self):
        return {
            'articles:category-detail': (self.object.pk,),
            'articles:category-articles-list': (self.object.pk,),
        }


class CategoryCreateView(CreateView):
    page_title = _("Create Category")
    model = Category
    fields = ['name']
    permission_required = 'add_category'

    def get_success_url(self):
        return reverse('articles:category-detail', args=(self.object.pk,))


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('articles:category-list')
    permission_required = 'delete_category'


class TagListView(ListView):
    page_title = _("Tags")
    model = Tag
    fields = ['term']
    field_links = {
        'term': 'articles:tag-detail',
    }
    tool_links = [
        (_('Create Tag'), 'articles:tag-create'),
    ]
    permission_required = 'view_tag'


class TagUpdateView(UpdateView):
    page_title = _("Edit Tag")
    model = Tag
    success_url = reverse_lazy('articles:tag-list')
    permission_required = 'change_tag'


class TagCreateView(CreateView):
    page_title = _("Create Tag")
    model = Tag
    fields = ['term']
    permission_required = 'add_tag'

    def get_success_url(self):
        return reverse('articles:tag-detail', args=(self.object.pk,))


class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy('articles:tag-list')
    permission_required = 'delete_tag'
