from django.conf.urls import url

from articles.views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleListView,
    ArticleUpdateView,
    CategoryArticlesListView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryListView,
    CategoryUpdateView,
    TagCreateView,
    TagDeleteView,
    TagListView,
    TagUpdateView,
)

app_name = "articles"

urlpatterns = [
    url(r"^$", ArticleListView.as_view(), name="list"),
    url(r"^create/$", ArticleCreateView.as_view(), name="create"),
    url(r"^(?P<pk>\d+)/$", ArticleUpdateView.as_view(), name="detail"),
    url(r"^(?P<pk>\d+)/delete/$", ArticleDeleteView.as_view(), name="delete"),
    url(r"^category/$", CategoryListView.as_view(), name="category-list"),
    url(
        r"^category/create/$",
        CategoryCreateView.as_view(),
        name="category-create",
    ),
    url(
        r"^category/(?P<pk>\d+)/$",
        CategoryUpdateView.as_view(),
        name="category-detail",
    ),
    url(
        r"^category/articles/(?P<pk>\d+)/$",
        CategoryArticlesListView.as_view(),
        name="category-articles-list",
    ),
    url(
        r"^category/(?P<pk>\d+)/delete/$",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    url(r"^tags/$", TagListView.as_view(), name="tag-list"),
    url(r"^tags/create/$", TagCreateView.as_view(), name="tag-create"),
    url(r"^tags/(?P<pk>\d+)/$", TagUpdateView.as_view(), name="tag-detail"),
    url(
        r"^tags/(?P<pk>\d+)/delete/$",
        TagDeleteView.as_view(),
        name="tag-delete",
    ),
]
