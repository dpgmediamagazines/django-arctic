import pytest
from django.urls import reverse

from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestOrderingView(object):
    """
    Test ListView using ArticleListView from example application
    """
    def _request(self, admin_client):
        response = admin_client.get(reverse('articles:list'),
                                    data={'order': '-category__name'})
        assert response.status_code == 200
        return response

    def test_virtual_ordering_field(self, admin_client):
        """
        Single item in ListView
        """
        ArticleFactory(title='Article 0')
        ArticleFactory(title='Article 1')
        response = self._request(admin_client)
        for key, item in response.context_data.items():
            print(key, item)
        assert response.context_data['list_header'][3]['order_url'] == \
               '/articles/?order=category__name'
        assert response.context_data['list_header'][3]['order_direction'] == \
               'desc'
        assert len(response.context_data['list_items']) == 2
        assert response.context_data['list_items'][0][0]['value'] == \
               'Article 1'
        assert response.context_data['list_items'][1][0]['value'] == \
               'Article 0'
