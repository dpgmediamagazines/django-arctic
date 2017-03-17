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

    def test_login_success_redirect_no_next(self, admin_user):
        """
        Asserts that an admin user is redirected to root after login,
        when no 'next' query param is given.

        :param admin_user: fixture provided by pytest-django
        :return: void
        """
        response = self.client.post('/login/',
                                    {
                                        'username': 'admin',
                                        'password': 'password'
                                    })

        assert response.status_code == 302
        assert response.url in ('/', 'http://testserver/')

    def test_login_success_redirect_next(self, admin_user):
        """
        Asserts that an admin user is redirected to the next page after
        login, when a 'next' query param is given.

        :param admin_user: fixture provided by pytest-django
        :return: void
        """
        response = self.client.post('/login/?next=/articles/',
                                    {
                                        'username': 'admin',
                                        'password': 'password'
                                    })

        assert response.status_code == 302
        assert response.url in ('/articles/', 'http://testserver/articles/')

    def test_login_success_redirect_next_other_host(self, admin_user):
        """
        Asserts that an admin user is redirected to root after login,
        when the 'next' query param refers to another host.

        :param admin_user: fixture provided by pytest-django
        :return: void
        """
        response = self.client.post('/login/?next=http://www.no.domain/test/',
                                    {
                                        'username': 'admin',
                                        'password': 'password'
                                    })

        assert response.status_code == 302
        assert response.url in ('/', 'http://testserver/')

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
