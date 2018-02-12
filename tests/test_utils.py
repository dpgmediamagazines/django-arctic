from collections import OrderedDict
import pytest
from django.urls import ResolverMatch, reverse
from django.http import HttpRequest

from arctic import utils
from tests.factories import ArticleFactory


@pytest.mark.django_db
class TestMenu:
    OUTPUT_MENU = OrderedDict([
        ('Dashboard', {
            'submenu': None, 'active': False,
            'active_weight': 1, 'icon': 'fa-dashboard', 'url': 'index'}
         ),
        ('Articles', {
            'submenu': OrderedDict([
                ('List', {'submenu': None, 'active': False,
                          'active_weight': 10, 'icon': None,
                          'url': 'articles:list'}
                 ),
                ('Create', {'submenu': None, 'active': False,
                            'active_weight': 17, 'icon': None,
                            'url': 'articles:create'})
            ]),
            'active': False,
            'active_weight': 0, 'icon': 'fa-file-text-o', 'url': None}
         ),
        ('Categories', {
            'submenu': OrderedDict([
                ('List', {'submenu': None, 'active': False,
                          'active_weight': 19, 'icon': None,
                          'url': 'articles:category-list'}
                 ),
                ('Create', {
                    'submenu': None, 'active': False,
                    'active_weight': 26, 'icon': None,
                    'url': 'articles:category-create'})
            ]),
            'active': False, 'active_weight': 0,
            'icon': 'fa-sitemap', 'url': None}
         ),
        ('Tags', {
            'submenu': OrderedDict([
                ('List', {'submenu': None, 'active': False,
                          'active_weight': 15, 'icon': None,
                          'url': 'articles:tag-list'}),
                ('Create', {'submenu': None, 'active': False,
                            'active_weight': 22, 'icon': None,
                            'url': 'articles:tag-create'})
            ]),
            'active': False, 'active_weight': 0,
            'icon': 'fa-tags', 'url': None}
         ),
        ('Users', {
            'submenu': OrderedDict([
                ('List', {'submenu': None, 'active': False,
                          'active_weight': 7, 'icon': None,
                          'url': 'users:list'}),
                ('Create', {'submenu': None, 'active': False,
                            'active_weight': 14, 'icon': None,
                            'url': 'users:create'})
            ]),
            'active': False, 'active_weight': 0,
            'icon': 'fa-user', 'url': None}
         ),
        ('Countries', {'submenu': None, 'active': False,
                       'active_weight': 11, 'icon': 'fa-globe',
                       'url': 'countries-list'})
    ])

    def test_menu(self, admin_user):
        """
        Test menu items with and without icons and with and without submenus
        """
        path = '/'
        request = HttpRequest()
        request.path = path
        request.resolver_match = ResolverMatch(None, None, None,
                                               url_name='index')
        request.user = admin_user
        kwargs = {'request': request, 'user': admin_user}

        menu = utils.menu(**kwargs)
        assert menu == self.OUTPUT_MENU

    def test_menu_on_detail_page(self, admin_client, admin_user):
        a = ArticleFactory()
        path = reverse('articles:detail', kwargs={'pk': a.id})
        request = HttpRequest()
        request.path = path
        request.resolver_match = ResolverMatch(None, None, None,
                                               url_name='detail',
                                               app_names=['articles'],
                                               namespaces=['articles'])
        request.user = admin_user
        kwargs = {'request': request, 'user': admin_user}

        menu = utils.menu(**kwargs)
        assert dict(menu)['Articles']['active'] is True

        articles_submenu = dict(dict(menu)['Articles']['submenu'])
        assert articles_submenu['List']['active'] is True
