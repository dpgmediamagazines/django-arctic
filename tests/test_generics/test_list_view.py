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
        lst_items = response.context_data['list_items']
        field = lst_items[0]['fields'][0]['field']
        assert lst_items[0]['fields'][0]['value'] == getattr(article, field)

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

    def test_two_tool_links(self, admin_client):
        """
        Single tool link display
        """
        response = self._request(admin_client)

        assert 'tool_links' in response.context_data
        assert len(response.context_data['tool_links']) == 2

    def test_multiple_tool_links(self, admin_client):
        """
        Multiple tool links display
        """
        ArticleListView.tool_links.append(('Create', 'articles:create'))

        response = self._request(admin_client)

        assert 'tool_links' in response.context_data
        assert len(response.context_data['tool_links']) == 3

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

        list_items = response.context_data['list_items']
        assert len(list_items) == 1
        assert list_items[0]['fields'][0]['value'] == 'title1'

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
        list_items = response.context_data['list_items']
        assert len(list_items) == 1
        assert list_items[0]['fields'][0]['value'] == 'title2'

    def test_simple_search_form_quick_filters(self, admin_client):
        """
        Test quick filters result
        """
        ArticleFactory(
            title='title1',
            description='description1',
            published=True
        )
        ArticleFactory(
            title='title2',
            description='Dead rabbit is walking without leg.',
            published=False
        )

        response = admin_client.get(reverse('articles:list'),
                                    {'published': 'published'})
        list_items = response.context_data['list_items']
        assert len(list_items) == 1
        assert list_items[0]['fields'][0]['value'] == 'title1'

        response = admin_client.get(reverse('articles:list'),
                                    {'published': 'drafts'})
        list_items = response.context_data['list_items']
        assert list_items[0]['fields'][0]['value'] == 'title2'

    def test_field_actions(self, admin_client):
        ArticleFactory(title='title1', description='description1',
                       published=True)
        ArticleFactory(title='title2', description='description2',
                       published=False)

        response = admin_client.get(reverse('articles:list'),
                                    {'description': ''})
        list_items = response.context_data['list_items']
        assert len(list_items[0]['actions']) == 1
        assert len(list_items[1]['actions']) == 2

    def test_field_actions_allowing(self, admin_client):
        def get_field_actions(self, obj):
            action_links = [
                ('detail', 'articles:detail', 'fa-edit'),
                ('categories', 'articles:category-list', 'fa-edit'),
            ]
            if not obj.published:
                action_links.append(
                    ('delete', 'articles:delete', 'fa-trash'), )
            return action_links

        ArticleListView.get_field_actions = get_field_actions

        ArticleFactory(title='title1', description='description1',
                       published=True)
        ArticleFactory(title='title2', description='description2',
                       published=False)

        response = admin_client.get(reverse('articles:list'),
                                    {'description': ''})
        list_items = response.context_data['list_items']
        assert len(list_items[0]['actions']) == 1
        assert len(list_items[1]['actions']) == 2

    def test_export_csv_file(self, admin_client):
        """
        Test csv file export functional
        """
        for i in range(30):
            ArticleFactory(title="title{}".format(i), description='description{}'.format(i))

        response = admin_client.get(reverse('articles:list'), {'format': 'csv'})
        assert response.status_code == 200
        assert response._headers['content-type'][1] == 'text/csv'
        attach_file = 'Articles.csv'
        assert attach_file in response._headers['content-disposition'][1]
        # 2 more rows in file: titles and blank line
        assert len(response._container) == 32
