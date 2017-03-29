import pytest
from django.core.urlresolvers import reverse

from articles.views import ArticleUpdateView
from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestArticleUpdate(object):

    def get_url(self, pk):
        return reverse('articles:detail', kwargs={'pk': pk})

    def test_update_page(self, admin_client):
        article = ArticleFactory()

        response = admin_client.get(self.get_url(article.pk))
        assert response.status_code == 200

    def test_readonly_fields(self, admin_client):
        article = ArticleFactory()
        view = ArticleUpdateView
        # Check with readonly field enabled
        view.readonly_fields = ['title']
        response = admin_client.get(self.get_url(article.pk))
        assert response.context_data['form'].fields['title']\
            .widget.attrs.get('readonly')

        # Check with readonly field disabled
        view.readonly_fields = []
        response = admin_client.get(self.get_url(article.pk))
        assert not response.context_data['form'].fields['title']\
            .widget.attrs.get('readonly')
