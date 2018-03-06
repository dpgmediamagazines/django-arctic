from __future__ import (absolute_import, unicode_literals)

from django.urls import (reverse, reverse_lazy)
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from arctic.generics import (CreateView, DeleteView, ListView, TemplateView,
                             UpdateView)
from collections import OrderedDict

from .forms import (ArticleForm, AdvancedArticleSearchForm,
                    FiltersAndSearchForm)
from .inlines import TagsInline
from .models import (Article, Category, Tag)


class DashboardView(TemplateView):
    template_name = 'arctic/index.html'
    page_title = 'Dashboard'
    permission_required = 'view_dashboard'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class ArticleListView(ListView):
    paginate_by = 10
    model = Article
    fields = ['title', 'description', 'published', 'category', 'tags']
    ordering_fields = ['title', 'description', 'category', 'published']
    search_fields = ['title']
    simple_search_form_class = FiltersAndSearchForm
    advanced_search_form_class = AdvancedArticleSearchForm
    breadcrumbs = (('Home', 'index'), ('Article List', None))
    action_links = [
        ('detail', 'articles:detail', 'fa-edit'),
        ('delete', 'articles:delete', 'fa-trash'),
    ]
    field_links = {
        'title': 'articles:detail',
        'category': ('articles:category-detail', 'category_id'),
    }
    tool_links = [
        (_('Create Article'), 'articles:create', 'fa-plus'),
    ]
    field_classes = {'published': ''}

    permission_required = "view_article"

    def get_category_field(self, row_instance):
        return row_instance.category.name

    def get_published_field(self, row_instance):
        symbol = 'fa-check' if row_instance.published else 'fa-minus'
        return mark_safe('<i class="fa {}"></i>'.format(symbol))

    def get_category_ordering_field(self):
        return 'category__name'

    def get_field_actions(self, row_instance):
        action_links = [
            ('detail', 'articles:detail', 'fa-edit'),
        ]
        if not row_instance.published:
            action_links.append(('delete', 'articles:delete', 'fa-trash'),)
        return action_links

    def get_published_field_classes(self, row_instance):
        return 'online' if row_instance.published else 'offline'


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
                         ['title', ['category', 'tags|5']]),
                        ('Body|Extra Information for this fieldset',
                         ['description']),
                        ('Extended Details',
                         [['published|4', 'updated_at']])])

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
                        ('+Basic Details',
                         ['title', ['category|4', 'tags']]),
                        ('-Body|Extra Information for this fieldset',
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
    sorting_field = 'order'
    action_links = [
        ('delete', 'articles:category-delete', 'fa-trash'),
    ]
    confirm_links = {
        'articles:category-delete': {
            'title': _('Delete "{{ name }}"'),
            'message': _('Are you sure you want to delete this?'),
            'ok': _('Delete'),
            'cancel': _('Cancel')}}


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
    fields = '__all__'
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
    redirect = True
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
    fields = '__all__'
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
