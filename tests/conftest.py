import pytest

from django.contrib.auth import get_user_model
from django.test import Client

from articles.models import Article, Category
from articles.forms import ArticleForm


User = get_user_model()


@pytest.fixture
def admin_client(admin_user):
    _client = Client()
    _client.force_login(User.objects.get(username='admin'))
    return _client


@pytest.fixture
def category():
    category = Category()
    category.name = 'name1'

    return category


@pytest.fixture
def article():
    article = Article()
    article.title = 'title1'
    article.description = 'description1'
    article.updated_at = 'updated_at1'
    article.category = category()
    article.published = 'published1'

    return article


@pytest.fixture
def article_form():
    article_form = ArticleForm()
    article_form.title = 'title'
    article_form.description = 'description'
    article_form.updated_at = 'updated_at'
    article_form.category = category()
    article_form.published = 'published'

    return article_form


def get_form(form):
    """
    This is a hack to make sure get_form returns what you expect
    the Django way. I don't know why get_form does not work yet.
    """
    def _get_form():
            return {field.name: field
                    for field in form}
    return _get_form

