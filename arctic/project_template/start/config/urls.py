from django.conf.urls import include, url

from arctic.generics import LoginView, LogoutView
from arctic.views import handler400, handler403, handler404  # noqa


urlpatterns = [
    url(r"^login/$", LoginView.as_view(), name="login"),
    url(r"^logout/$", LogoutView.as_view(), name="logout"),
    url(r"^arctic/", include("arctic.urls", namespace="arctic")),
    url(r"^", include("dashboard.urls")),
]
