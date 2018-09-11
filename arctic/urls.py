from django.conf.urls import url

from arctic.views import AutoCompleteView, OrderView, RedirectToParentView

app_name = "arctic"

urlpatterns = [
    url(
        r"^autocomplete/(?P<resource>[\w_]+)/(?P<search>[^/]*)$",
        AutoCompleteView.as_view(),
        name="autocomplete",
    ),
    url(r"^order/(?P<resource>[\w_\.]+)$", OrderView.as_view(), name="order"),
    url(
        r"^redirect-to-parent$",
        RedirectToParentView.as_view(),
        name="redirect_to_parent",
    ),
]
