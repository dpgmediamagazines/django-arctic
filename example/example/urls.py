# -*-*- encoding: utf-8 -*-*-
from __future__ import (absolute_import, unicode_literals)

from django.conf import settings
from django.conf.urls import (include, url)
from django.conf.urls.static import static

from arctic.generics import LoginView
from arctic.urls import autocomplete_url
from arctic.users.urls import user_patterns
from arctic.views import (handler400, handler403, handler404, handler500)  # noqa

from articles.views import (ArticleCreateView, ArticleDeleteView,
                            ArticleListView, ArticleUpdateView,
                            CategoryArticlesListView, CategoryCreateView,
                            CategoryDeleteView, CategoryListView,
                            CategoryUpdateView, TagCreateView, TagDeleteView,
                            TagListView, TagUpdateView)
from dashboard.views import DashboardView

article_patterns = [
    url(r'^$', ArticleListView.as_view(), name='list'),
    url(r'^create/$', ArticleCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', ArticleUpdateView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/delete/$', ArticleDeleteView.as_view(), name='delete'),
    url(r'^category/$', CategoryListView.as_view(), name='category-list'),
    url(r'^category/create/$', CategoryCreateView.as_view(),
        name='category-create'),
    url(r'^category/(?P<pk>\d+)/$', CategoryUpdateView.as_view(),
        name='category-detail'),
    url(r'^category/articles/(?P<pk>\d+)/$',
        CategoryArticlesListView.as_view(), name='category-articles-list'),
    url(r'^category/(?P<pk>\d+)/delete/$', CategoryDeleteView.as_view(),
        name='category-delete'),
    url(r'^tags/$', TagListView.as_view(), name='tag-list'),
    url(r'^tags/create/$', TagCreateView.as_view(), name='tag-create'),
    url(r'^tags/(?P<pk>\d+)/$', TagUpdateView.as_view(), name='tag-detail'),
    url(r'^tags/(?P<pk>\d+)/delete/$', TagDeleteView.as_view(),
        name='tag-delete'),
]

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^articles/', include(article_patterns, namespace='articles')),
    url(r'^users/', include(user_patterns, namespace='users')),
    autocomplete_url,
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
