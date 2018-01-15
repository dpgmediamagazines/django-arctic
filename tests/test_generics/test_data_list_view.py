import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestDataListView(object):
    """
    Test ListView using ArticleListView from example application
    """
    def _request(self, admin_client):
        response = admin_client.get(reverse('countries-list'))
        assert response.status_code == 200
        return response

    def _assert_list_items_len(self, response, length):
        assert 'list_items' in response.context_data
        assert len(response.context_data['list_items']) == length

    # def test_paginated_items(self, admin_client):
    #     """
    #     Paginated List view
    #     """
    #     response = self._request(admin_client)
    #     self._assert_list_items_len(response, 250)

    #     assert response.context_data['page_obj'].paginator.num_pages == 20

    # def test_simple_search_form(self, admin_client):
    #     # empty search, return all
    #     response = admin_client.get(reverse('countries-list'),
    #                                 {'search': ''})
    #     assert len(response.context_data['list_items']) == 150

    #     # search filled, filter content
    #     response = admin_client.get(reverse('countries-list'),
    #                                 {'search': 'af'})
    #     assert len(response.context_data['list_items']) == 3
