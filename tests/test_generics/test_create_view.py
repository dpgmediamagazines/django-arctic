import pytest

from django.core.urlresolvers import reverse


@pytest.mark.django_db
class TestCreateView(object):
    """
    Test CreateView using ArticleCreateView, CategoryCreateView 
    and TagCreateView from example application
    """
    @property
    def article_url(self):
        return reverse('articles:create')

    @property
    def category_url(self):
        return reverse('articles:category-create')

    @property
    def tag_url(self):
        return reverse('articles:tag-create')

    def test_create_article_page(self, admin_client):
        response = admin_client.get(self.article_url)
        assert response.status_code == 200

    def test_create_category_page(self, admin_client):
        response = admin_client.get(self.category_url)
        assert response.status_code == 200

    def test_create_tag_page(self, admin_client):
        response = admin_client.get(self.tag_url)
        assert response.status_code == 200

    def test_article_submit(self, admin_client):
        response = admin_client.post(
            self.article_url, {'title': 'Title_text',
                               'decsription': 'Description_text',
                               'published': True}
        )
        assert response.status_code == 200

    def test_category_submit(self, admin_client):
        response = admin_client.post(
            self.category_url, {'name': 'test_category'}
        )
        assert response.status_code == 302

    def test_tag_submit(self, admin_client):
        response = admin_client.post(
            self.tag_url, {'term': 'test_tag'}
        )
        assert response.status_code == 302
