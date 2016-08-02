from django.conf.urls import include, url

from .views import UserListView, UserCreateView, UserUpdateView


user_patterns = [
    url(r'^$', UserListView.as_view(), name='list'),
    url(r'^create/$', UserCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', UserUpdateView.as_view(), name='detail'),
]
