from collections import OrderedDict
# import django.core.urlresolvers
# from django.http import HttpRequest
#
# from arctic import utils


class TestMenu:
    MENU = (
        ('menu 1', 'url_1', 'icon 1'),
        ('menu 2', 'url_2', 'icon 2', (
            ('menu 2_1', 'url_2_1'),
            ('menu 2_2', 'url_2_2'),
        )),
        ('menu 3', '/'),
        ('menu 4', 'url_4', (
            ('menu 4_1', 'url_4_1', 'icon 4_1'),
        )),
    )

    OUTPUT_MENU = OrderedDict([
        ('menu 1', {'url': 'url_1', 'icon': 'icon 1', 'active': False,
                    'active_weight': 5, 'submenu': None}),
        ('menu 2', {'url': 'url_2', 'icon': 'icon 2', 'active': False,
                    'active_weight': 5, 'submenu': OrderedDict([
            ('menu 2_1', {'url': 'url_2_1', 'icon': None, 'active': False,
                          'active_weight': 7, 'submenu': None}),
            ('menu 2_2', {'url': 'url_2_2', 'icon': None, 'active': False,
                          'active_weight': 7, 'submenu': None}),
        ])}),
        ('menu 3', {'url': '/', 'icon': None, 'active': True,
                    'active_weight': 1, 'submenu': None}),
        ('menu 4', {'url': 'url_4', 'icon': None, 'active': False,
                    'active_weight': 5, 'submenu': OrderedDict([
            ('menu 4_1', {'url': 'url_4_1', 'icon': 'icon 4_1',
                          'active': False, 'active_weight': 7,
                          'submenu': None}),
        ])}),
    ])  # noqa

    # def test_menu(self, monkeypatch):
    #     """
    #     Test menu items with and without icons and with and without submenus
    #     """
    #     request = HttpRequest()
    #     request.path = '/'
    #     kwargs = {'request': request}
    #
    #     monkeypatch.setattr(django.core.urlresolvers, 'reverse',
    #                         lambda url: url)
    #     menu = utils.menu(menu_config=self.MENU, **kwargs)
    #
    #     assert menu == self.OUTPUT_MENU
