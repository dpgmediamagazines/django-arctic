# -*-*- encoding: utf-8 -*-*-
from __future__ import (absolute_import, unicode_literals)

from django.conf import settings
from django.conf.urls import (include, url)
from django.conf.urls.static import static

from arctic.generics import LoginView
from arctic.urls import autocomplete_url
from arctic.users.urls import user_patterns
from arctic.views import (handler400, handler403, handler404, handler500)  # noqa

from countries.views import (CountryAPIView, CountryListView)
from dashboard.views import DashboardView

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^articles/', include('articles.urls', 'articles')),
    url(r'^users/', include(user_patterns, namespace='users')),
    url(r'^countries/$', CountryListView.as_view(), name='countries-list'),
    url(r'^countries-api/$', CountryAPIView.as_view(), name='countries-api'),
    autocomplete_url,
]


if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
