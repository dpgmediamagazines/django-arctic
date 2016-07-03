# -*-*- encoding: utf-8 -*-*-
# pylint: disable=E1101
from __future__ import unicode_literals, absolute_import
import importlib

from collections import OrderedDict
from django.conf import settings
from django.core import urlresolvers


def is_active(path, path_to_check):
    return path.startswith(path_to_check)

# TODO: menu needs to hide entries not available to a certain user role
# by getting the view class from the named url we can check which permissions
# are available:
# http://stackoverflow.com/questions/5749075

def menu(menu_config=None, **kwargs):
    """
    Tranforms a menu definition into a dictionary which is a frendlier format
    to parse in a template.
    """
    request = kwargs.pop('request', None)
    user = kwargs.pop('user', None)

    if not menu_config:
        menu_config = settings.ARCTIC_MENU

    menu_dict = OrderedDict()
    for menu_entry in menu_config:
        if type(menu_entry) in (list, tuple):
            path = urlresolvers.reverse(menu_entry[1])
            # icons are optional
            icon = None
            if (len(menu_entry) >= 3) and \
               (not type(menu_entry[2]) in (list, tuple)):
                icon = menu_entry[2]
            menu_dict[menu_entry[0]] = {
                'url': menu_entry[1],
                'icon': icon,
                'submenu': None,
                'active': is_active(request.path, path),
                'active_weight': len(path)
            }

            # check if the last item in a menu entry is a submenu
            last_item = menu_entry[-1]
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


def view_from_url(named_url):
    """
    Finds and returns the view class from a named url
    """
    view_func = urlresolvers.resolve(urlresolvers.reverse(named_url)).func
    module = importlib.import_module(view_func.__module__)
    view = getattr(module, view_func.__name__)

    return view


def find_attribute(obj, value):
    """
    Finds the attribute connected to the last object when a chain of
    connected objects is given in a string separated with double underscores.
    For example when a model x has a foreign key to model y and model y has
    attribute a, findattr(x, 'y__a') will return the a attribute from the y
    model that exists in x.
    """
    if '__' in value:
        value_list = value.split('__')
        attr = getattr(obj, value_list[0])
        return find_attribute(attr, '__'.join(value_list[1:]))
    return getattr(obj, value)


def find_field_meta(obj, value):
    """
    In a model, finds the attribute meta connected to the last object when
    a chain of  connected objects is given in a string separated with double
    underscores.
    """
    if '__' in value:
        value_list = value.split('__')
        child_obj = obj._meta.get_field(value_list[0]).rel.to
        return find_field_meta(child_obj, '__'.join(value_list[1:]))
    return obj._meta.get_field(value)
