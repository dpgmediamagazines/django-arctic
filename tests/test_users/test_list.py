import pytest

from django.core.urlresolvers import reverse

from tests.factories import UserFactory


@pytest.mark.django_db
class TestUserList(object):

    @property
    def url(self):
        return reverse('users:list')

    def test_user_list(self, admin_client):
        [UserFactory() for i in range(10)]
        response = admin_client.get(self.url)
        assert response.status_code == 200
