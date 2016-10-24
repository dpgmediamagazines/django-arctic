import pytest
from django.core.exceptions import PermissionDenied
from django.test import Client


class TestCMS(object):
    """
    Tests that probe the CMS with the Django test client
    """

    @pytest.fixture(scope="session", autouse=True)
    def init(self):
        self.__class__.client = Client()

    def test_login_success(self, admin_user):
        """
        Asserts that an admin user can log in an see a restricted page
        within the CMS

        :param admin_user: fixture provided by pytest-django
        :return: void
        """
        self.client.post('/login/',
                         {
                             'username': 'admin',
                             'password': 'password'
                         })
        response = self.client.get('/articles/')

        assert response.status_code == 200

    def test_login_fail(self, admin_user):
        """
        Asserts that an unauthorized user cannot see a restricted page

        :return:
        """
        try:
            response = self.client.get('/articles/')
            assert response.status_code != 200
        except PermissionDenied:
            assert True
