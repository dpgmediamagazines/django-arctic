# -*-*- encoding: utf-8 -*-*-
# pylint: disable=E1101
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from django.conf import settings
from django.core.urlresolvers import reverse


def is_active(path, path_to_check):
    return path.startswith(path_to_check)


# TODO: menu needs to hide entries not available to a certain user role
# by getting the view class from the named url we can check which permissions
# are available:
# http://stackoverflow.com/questions/5749075

def menu(menu_config=None, **kwargs):
    request = kwargs.pop('request', None)
    user = kwargs.pop('user', None)

    if not menu_config:
        menu_config = settings.ARCTIC_MENU

    menu_dict = OrderedDict()
    for menu_entry in menu_config:
        if type(menu_entry) in (list, tuple):
            path = reverse(menu_entry[1])
            menu_dict[menu_entry[0]] = {
                'url': menu_entry[1],
                'icon': menu_entry[2],
                'submenu': None,
                'active': is_active(request.path, path),
                'active_weight': len(path)
            }

            # check if the last item in a menu entry is a submenu
            last_item = menu_entry[len(menu_entry) - 1]
            if type(last_item) in (list, tuple):
                menu_dict[menu_entry[0]]['submenu'] = menu(last_item,
                                                           user=user,
                                                           request=request)

    return menu_clean(menu_dict)


def menu_clean(menu_config):
    """
    Make sure that only the menu item with the largest weight is active.
    If a child of a menu item is active, the parent should be active too.
    :param menu:
    :return:
    """
    max_weight = -1
    for _, value in list(menu_config.items()):
        if value['submenu']:
            for _, v in list(value['submenu'].items()):
                if v['active']:
                    # parent inherits the weight of the axctive child
                    value['active'] = True
                    value['active_weight'] = v['active_weight']

        if value['active']:
            max_weight = max(value['active_weight'], max_weight)

    if max_weight > 0:
        # one of the items is active: make items with lesser weight inactive
        for _, value in list(menu_config.items()):
            if value['active'] and value['active_weight'] < max_weight:
                max_weight = max(value['active_weight'], max_weight)
                value['active'] = False
    return menu_config
