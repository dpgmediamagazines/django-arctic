import pytest

from django.urls import reverse

from articles.views import ArticleListView
from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestListView(object):
    """
    Test ListView using ArticleListView from example application
    """
    def _request(self, admin_client):
        response = admin_client.get(reverse('articles:list'))
        assert response.status_code == 200
        return response

    def _assert_list_items_len(self, response, length):
        assert 'list_items' in response.context_data
        assert len(response.context_data['list_items']) == length

    def test_single_item(self, admin_client):
        """
        Single item in ListView
        """
        article = ArticleFactory()
        response = self._request(admin_client)
        self._assert_list_items_len(response, 1)
        field = response.context_data['list_items'][0][0]['field']
        assert response.context_data['list_items'][0][0]['value'] == \
            getattr(article, field)

    def test_paginated_items(self, admin_client):
        """
        Paginated List view
        """
        [ArticleFactory() for i in range(30)]

        response = self._request(admin_client)
        self._assert_list_items_len(response, 10)

        assert response.context_data['page_obj'].paginator.num_pages == 3

    def test_no_items(self, admin_client):
        """
        No items in ListView
        """
        response = self._request(admin_client)

        self._assert_list_items_len(response, 0)

    def test_one_tool_link(self, admin_client):
        """
        Single tool link display
        """
        response = self._request(admin_client)

        assert 'tool_links' in response.context_data
        assert len(response.context_data['tool_links']) == 1

    def test_multiple_tool_links(self, admin_client):
        """
        Multiple tool links display
        """
        ArticleListView.tool_links.append(('Delete', 'articles:delete'))

        response = self._request(admin_client)

        assert 'tool_links' in response.context_data
        assert len(response.context_data['tool_links']) == 2

    def test_no_tool_links(self, admin_client):
        """
        Handling case with no tool links
        """
        ArticleListView.tool_links = []

        response = self._request(admin_client)

        assert 'tool_links' in response.context_data
        assert len(response.context_data['tool_links']) == 0

    def test_simple_search_form(self, admin_client):
        """
        Test simple search form
        """
        ArticleFactory(title='title1')
        ArticleFactory(title='title2')

        # empty search, return all
        response = admin_client.get(reverse('articles:list'), {'search': ''})
        assert len(response.context_data['list_items']) == 2

        # search filled, filter content
        response = admin_client.get(reverse('articles:list'),
                                    {'search': 'le1'})
        assert len(response.context_data['list_items']) == 1
        assert response.context_data['list_items'][0][0]['value'] == 'title1'

    def test_advanced_search_form(self, admin_client):
        """
        Test simple search form
        """
        ArticleFactory(title='title1', description='description1')
        ArticleFactory(title='title2', description='description2')

        # empty search, return all
        response = admin_client.get(reverse('articles:list'),
                                    {'description': ''})
        assert len(response.context_data['list_items']) == 2

        # search filled, filter content
        response = admin_client.get(reverse('articles:list'),
                                    {'description': 'tion2'})
        assert len(response.context_data['list_items']) == 1
        assert response.context_data['list_items'][0][0]['value'] == 'title2'
