import pytest

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def admin_client(admin_user):
    """
    Get Django client with logged in admin user
    """
    _client = Client()
    _client.login(username='admin', password='password')
    return _client


def get_form(form):
    """
    This is a hack to make sure get_form returns what you expect
    the Django way. I don't know why get_form does not work yet.
    """
    def _get_form():
            return {field.name: field for field in form}
    return _get_form
