from django.test import Client
import pytest
from bs4 import BeautifulSoup


class TestLogin:

    @pytest.fixture(scope="session")
    def init(self):
        self.client = Client()

    def _login(self):
        self.client = Client()
        self.client.post('/login/', {'username': 'admin', 'password': 'password'})

    def test_login(self, admin_user):
        self._login()
        response = self.client.get('/articles/')

        assert response.status_code == 200

        # print(BeautifulSoup(response.content).prettify())


    # def test_listCategories(self, admin_user):
    #     self._login()
    #     response = self.client.get('/articles/category/')
    #
    #     soup = BeautifulSoup(response.content)
    #
    #     # print(soup.prettify())
