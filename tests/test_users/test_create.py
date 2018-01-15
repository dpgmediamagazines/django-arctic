import pytest

from arctic.models import Role
from django.urls import reverse

from tests.factories import UserFactory


@pytest.mark.django_db
class TestUserCreate(object):
    @property
    def url(self):
        return reverse('users:create')

    def test_create_page(self, admin_client):
        response = admin_client.get(self.url)
        assert response.status_code == 200

    def test_user_submit(self, django_user_model, admin_client):
        assert django_user_model.objects.count() == 1

        username = 'u1'
        email = 'u1@test.test'

        response = admin_client.post(
            self.url, {'user-username': username,
                       'user-email': email,
                       'user-password1': 'qqqqqq22222',
                       'user-password2': 'qqqqqq22222',
                       'user-is_active': True,
                       'role-role': Role.objects.all()[0].pk}
        )
        assert response.status_code == 302
        assert django_user_model.objects.count() == 2
        user = django_user_model.objects.filter(
            username=username, email=email).first()
        assert user is not None

    def test_user_exist_submit(self, django_user_model, admin_client):
        username = 'u1'
        email = 'u1@test.test'
        UserFactory(username=username, email=email)
        assert django_user_model.objects.count() == 2

        response = admin_client.post(
            self.url, {'user-username': username,
                       'user-email': email,
                       'user-password1': 'qqqqqq22222',
                       'user-password2': 'qqqqqq22222',
                       'user-is_active': True,
                       'role-role': Role.objects.all()[0].pk}
        )
        assert response.status_code == 200
        assert django_user_model.objects.count() == 2
