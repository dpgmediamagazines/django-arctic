import pytest

from arctic.models import Role
from django.urls import reverse

from tests.factories import UserFactory


@pytest.mark.django_db
class TestUserUpdate(object):

    def get_url(self, pk):
        return reverse('users:detail', kwargs={'pk': pk})

    def test_update_page(self, admin_client):
        user = UserFactory()

        response = admin_client.get(self.get_url(user.pk))
        assert response.status_code == 200

    def test_user_submit(self, django_user_model, admin_client):
        user = UserFactory(username='u1', email='u1@test.test')

        username = 'u1-changed'
        email = 'u1-changed@test.test'

        response = admin_client.post(
            self.get_url(user.pk),
            {'user-email': email,
             'role-role': str(Role.objects.get(name='editor').pk),
             'user-username': username, }
        )

        assert response.status_code == 302
        user = django_user_model.objects.get(pk=user.pk)
        assert user.email == email
        assert user.username == username
