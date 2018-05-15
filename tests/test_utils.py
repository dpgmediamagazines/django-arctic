from collections import OrderedDict
import pytest
from django.urls import ResolverMatch, reverse
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _

from arctic import utils


@pytest.mark.django_db
class TestMenu:
    OUTPUT_MENU = OrderedDict([
        (_('Dashboard'), {
            'submenu': None, 'active': False,
            'active_weight': 1, 'icon': 'fa-dashboard', 'url': 'index'}
         ),
        (_('Articles'), {
            'submenu': OrderedDict([
                (_('List'), {'submenu': None,
                             'active': False,
                             'active_weight': 10, 'icon': None,
                             'url': 'articles:list'}),
                (_('Create'), {'submenu': None, 'active': False,
                               'active_weight': 17, 'icon': None,
                               'url': 'articles:create'})
            ]),
            'active': False,
            'active_weight': 0, 'icon': 'fa-file-text-o', 'url': None}
         ),
        (_('Categories'), {
            'submenu': OrderedDict([
                (_('List'), {'submenu': None, 'active': False,
                             'active_weight': 19, 'icon': None,
                             'url': 'articles:category-list'}
                 ),
                (_('Create'), {
                    'submenu': None, 'active': False,
                    'active_weight': 26, 'icon': None,
                    'url': 'articles:category-create'})
            ]),
            'active': False, 'active_weight': 0,
            'icon': 'fa-sitemap', 'url': None}
         ),
        (_('Tags'), {
            'submenu': OrderedDict([
                (_('List'), {'submenu': None, 'active': False,
                             'active_weight': 15, 'icon': None,
                             'url': 'articles:tag-list'}),
                (_('Create'), {'submenu': None, 'active': False,
                               'active_weight': 22, 'icon': None,
                               'url': 'articles:tag-create'})
            ]),
            'active': False, 'active_weight': 0,
            'icon': 'fa-tags', 'url': None}
         ),
        (_('Users'), {
            'submenu': OrderedDict([
                (_('List'), {'submenu': None, 'active': False,
                             'active_weight': 7, 'icon': None,
                             'url': 'users:list'}),
                (_('Create'), {'submenu': None, 'active': False,
                               'active_weight': 14, 'icon': None,
                               'url': 'users:create'})
            ]),
            'active': False, 'active_weight': 0,
            'icon': 'fa-user', 'url': None}
         ),
        (_('Countries'), {'submenu': None, 'active': False,
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

    def test_menu_on_detail_page(self, admin_user):
        path = reverse('articles:detail', kwargs={'pk': 1})
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

    def test_is_active_menu_item(self):
        MENU_CONF = (
            ('Articles', None, 'fa-file-text-o', (
                ('List', 'articles:list', ('articles:detail',)),
                ('Create', 'articles:create')
            ), ('articles:delete',)),
        )
        is_menu_active = utils.is_active(MENU_CONF[0], 'articles:delete')
        is_submenu_active = utils.is_active(MENU_CONF[0][-2][0],
                                            'articles:delete')
        assert is_menu_active is True
        assert is_submenu_active is False
