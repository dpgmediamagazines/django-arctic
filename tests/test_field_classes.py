import pytest
from django.urls import reverse

from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestFieldClasses(object):
    def _request(self, admin_client):
        response = admin_client.get(reverse('articles:list'))
        assert response.status_code == 200
        return response

    def test_field_classes(self, admin_client):
        """
        Virtual field displayed in ListView
        """
        ArticleFactory(published=True)
        ArticleFactory(published=False)
        response = self._request(admin_client)

        list_items = response.context_data['list_items']
        assert list_items[0]['fields'][2]['class'] == 'online'
        assert list_items[1]['fields'][2]['class'] == 'offline'
