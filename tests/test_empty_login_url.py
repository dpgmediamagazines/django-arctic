import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse


@pytest.mark.django_db
class TestEmptyLogin(object):
    def test_empty_login_and_logout_with_no_required_login(
            self, client, settings
    ):
        settings.LOGIN_URL = None
        settings.LOGOUT_URL = None
        response = client.get(reverse('index'))
        assert response.status_code == 200

    def test_empty_login_and_logout_with_required_login(
            self, client, settings
    ):
        settings.LOGIN_URL = None
        settings.LOGOUT_URL = None

        with pytest.raises(ImproperlyConfigured):
            client.get(reverse('articles:list'))
