from django.conf.urls import url

from arctic.views import AutoCompleteView


autocomplete_url = \
    url(r'^autocomplete/(?P<resource>[\w_]+)/(?P<search>[^/]*)$',
        AutoCompleteView.as_view(), name='autocomplete')
