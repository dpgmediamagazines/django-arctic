from django.conf.urls import url

from arctic.views import AutoCompleteView, OrderView

app_name = 'arctic'

urlpatterns = [
    url(r'^autocomplete/(?P<resource>[\w_]+)/(?P<search>[^/]*)$',
        AutoCompleteView.as_view(), name='autocomplete'),
    url(r'^order/(?P<resource>[\w_\.]+)$',
        OrderView.as_view(), name='order'),
]
