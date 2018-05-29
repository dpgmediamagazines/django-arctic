import pytest
from django.urls import reverse

from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestOrderingView(object):
    """
    Test ordering on ListView
    """
    def _request(self, admin_client):
        response = admin_client.get(reverse('articles:list'),
                                    data={'order': '-category__name'})
        assert response.status_code == 200
        return response

    def test_virtual_ordering_field(self, admin_client):
        """
        ordering by 'virtual ordering field'
        """
        ArticleFactory(title='Article 0')
        ArticleFactory(title='Article 1')
        response = self._request(admin_client)
        lst_headers = response.context_data['list_header']
        lst_items = response.context_data['list_items']
        assert lst_headers[3]['order_url'] == '/articles/?order=category__name'
        assert lst_headers[3]['order_direction'] == 'desc'
        assert len(lst_items) == 2
        assert lst_items[0]['fields'][0]['value'] == 'Article 1'
        assert lst_items[1]['fields'][0]['value'] == 'Article 0'
