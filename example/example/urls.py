# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from articles.views import (
    ArticleListView, ArticleCreateView,
    ArticleDetailView, ArticleDeleteView)
from dashboard.views import DashboardView

article_patterns = [
    url(r'^$', ArticleListView.as_view(), name='list'),
    url(r'^create/$', ArticleCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/delete/$', ArticleDeleteView.as_view(), name='delete'),
]

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='index'),
    url(r'^articles/', include(article_patterns, namespace='articles')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
