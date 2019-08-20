from django.conf.urls import url

from . import views

app_name = "{{ app_name }}"

urlpatterns = [url(r"^$", views.{{ camel_case_app_name }}ListView.as_view(), name="list"),
               url(r"^create/$", views.{{ camel_case_app_name }}CreateView.as_view(), name="create"),
               url(r"^(?P<pk>\d+)/$", views.{{ camel_case_app_name }}UpdateView.as_view(), name="detail"),
               url(r"^(?P<pk>\d+)/delete/$", views.{{ camel_case_app_name }}DeleteView.as_view(), name="delete"),
               ]
