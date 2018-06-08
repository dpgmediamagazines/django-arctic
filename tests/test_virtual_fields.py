import pytest

from django.urls import reverse

from articles.views import ArticleListView
from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestVirtualFields(object):
    def _request(self, admin_client):
        response = admin_client.get(reverse('articles:list'))
        assert response.status_code == 200
        return response

    def _assert_list_items_len(self, response, length):
        assert 'list_items' in response.context_data
        assert len(response.context_data['list_items']) == length

    def test_virtual_field(self, admin_client):
        """
        Virtual field displayed in ListView
        """
        article = ArticleFactory()
        view = ArticleListView()
        view.fields = ['title', 'description', 'published', 'category']
        response = self._request(admin_client)
        self._assert_list_items_len(response, 1)

        item = response.context_data['list_items'][0]
        assert item['fields'][0]['value'] == article.title
        assert item['fields'][1]['value'] == article.description
        assert item['fields'][3]['value'] == article.category.name

    def test_missing_virtual_field(self, admin_client):
        """
        Error happens on wrong virtual field name
        """
        article = ArticleFactory()  # noqa
        view = ArticleListView()
        view.fields = ['title', 'description', 'published', 'virtual_field']
        response = self._request(admin_client)

        search_virtual_field = False
        for field in response.context_data['list_items'][0]['fields']:
            if field['type'] == 'field' and 'virtual_field' in field['field']:
                search_virtual_field = True

        assert search_virtual_field is False

    def test_missing_virtual_field_error(self, admin_client):
        """
        Error happens on wrong virtual field name
        """
        article = ArticleFactory()
        view = ArticleListView()
        view.fields = ['title', 'description', 'published', 'virtual_field']

        exc = pytest.raises(
            AttributeError, view.get_field_value, 'virtual_field', article)

        assert str(exc.value) == \
            "'Article' object has no attribute 'virtual_field'", \
            exc.value.message

    def test_missing_virtual_field_execution_attribute_error(self,
                                                             admin_client):
        """
        Error happens on wrong virtual field name
        """
        article = ArticleFactory()
        view = ArticleListView()
        view.fields = ['title', 'description', 'published', 'broken']
        view.get_broken_field = lambda obj: obj.unknown_field
        exc = pytest.raises(
            AttributeError, view.get_field_value, 'broken', article)
        assert str(exc.value) == \
            "'Article' object has no attribute 'unknown_field'", \
            exc.value.message
