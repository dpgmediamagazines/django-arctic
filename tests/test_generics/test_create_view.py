import pytest

from django.core.urlresolvers import reverse
from articles.models import Article, Category, Tag
from tests.factories import CategoryFactory, TagFactory


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
        CategoryFactory()
        TagFactory()
        cat_id = Category.objects.all()[0].pk
        tag_id = Tag.objects.all()[0].pk
        response = admin_client.post(
            self.article_url, {'title': 'Title_text',
                               'decsription': 'Description_text',
                               'published': True,
                               'category': cat_id,
                               'tags': tag_id,
                               'updated_at': '11-11-2016 10:53'}
        )
        articles_obj = Article.objects.count()
        assert response.status_code == 302
        assert articles_obj == 1

    def test_category_submit(self, admin_client):
        response = admin_client.post(
            self.category_url, {'name': 'test_category'}
        )
        category_obj = Category.objects.count()
        assert response.status_code == 302
        assert category_obj == 1

    def test_tag_submit(self, admin_client):
        response = admin_client.post(
            self.tag_url, {'term': 'test_tag'}
        )
        tag_obj = Tag.objects.count()
        assert response.status_code == 302
        assert tag_obj == 1
