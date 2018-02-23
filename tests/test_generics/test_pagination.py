import pytest
from django.urls import reverse
from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestPagination(object):
    """
    Test Arctic pagination
    """
    def test_paginated_list(self, admin_client):
        [ArticleFactory() for i in range(20)]
        response = admin_client.get("%s?page=2" % reverse('articles:list'))
        assert response.status_code == 200

    def test_page_out_of_list(self, admin_client):
        [ArticleFactory() for i in range(20)]
        response = admin_client.get("%s?page=20" % reverse('articles:list'))
        assert response.status_code == 404
