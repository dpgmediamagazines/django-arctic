from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
from copy import deepcopy
import importlib

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.urls import (
    get_ns_resolver,
    get_resolver,
    get_urlconf,
    NoReverseMatch,
    reverse,
)
from django.template.defaultfilters import slugify
from django.utils import translation

from . import defaults


def is_active(menu_entry, url_name):
    if url_name:
        if menu_entry[1] == url_name:
            return True
        elif len(menu_entry) >= 3:
            related_urls = []
            related_submenus = []

            for menu_item in menu_entry[2:]:
                if is_list_of_list(menu_item):
                    # suppose it is submenus
                    related_submenus = menu_item
                elif isinstance(menu_item, (tuple, list)):
                    # suppose it is related urls names
                    related_urls += list(menu_item)
            related_urls += [submenu[1] for submenu in related_submenus]
            if url_name in related_urls:
                return True
            # Check for * in the related url's
            start_url = []
            for related in related_urls:
                if related.endswith('*'):
                    start_url += [related]
            if len(start_url):
                url_base_name = url_name.split(':')
                del url_base_name[-1]
                url_base_name = ':'.join(url_base_name)
                for item in start_url:
                    return item.startswith(url_base_name)
    return False


# TODO: menu needs to hide entries not available to a certain user role
# by getting the view class from the named url we can check which permissions
# are available:
# http://stackoverflow.com/questions/5749075


def menu(menu_config=None, **kwargs):
    """
    Tranforms a menu definition into a dictionary which is a frendlier format
    to parse in a template.
    """
    request = kwargs.pop("request", None)
    user = kwargs.pop("user", None)
    url_full_name = ":".join(
        [request.resolver_match.namespace, request.resolver_match.url_name]
    )

    if not menu_config:
        menu_config = settings.ARCTIC_MENU

    menu_dict = OrderedDict()
    for menu_entry in menu_config:
        if type(menu_entry) in (list, tuple):

            # check permission based on named_url
            path = None
            if menu_entry[1]:
                if not view_from_url(menu_entry[1]).has_permission(user):
                    continue

                path = reverse(menu_entry[1])
            # icons and collapse are optional
            icon = None
            if (len(menu_entry) >= 3) and (
                not type(menu_entry[2]) in (list, tuple)
            ):
                icon = menu_entry[2]
            active_weight = len(path) if path else 0
            menu_dict[menu_entry[0]] = {
                "url": menu_entry[1],
                "icon": icon,
                "submenu": None,
                "active": is_active(menu_entry, url_full_name),
                "active_weight": active_weight,
            }

            # check if the last item in a menu entry is a submenu
            submenu = _get_submenu(menu_entry)
            if submenu:
                menu_dict[menu_entry[0]]["submenu"] = menu(
                    submenu, user=user, request=request
                )
    return menu_clean(menu_dict)


def _get_submenu(menu_entry):
    for item in menu_entry[-2:]:
        if is_list_of_list(item):
            return item


def menu_clean(menu_config):
    """
    Make sure that only the menu item with the largest weight is active.
    If a child of a menu item is active, the parent should be active too.
    :param menu:
    :return:
    """
    max_weight = -1
    for _, value in list(menu_config.items()):
        if value["submenu"]:
            for _, v in list(value["submenu"].items()):
                if v["active"]:
                    # parent inherits the weight of the axctive child
                    value["active"] = True
                    value["active_weight"] = v["active_weight"]

        if value["active"]:
            max_weight = max(value["active_weight"], max_weight)

    if max_weight > 0:
        # one of the items is active: make items with lesser weight inactive
        for _, value in list(menu_config.items()):
            if value["active"] and value["active_weight"] < max_weight:
                value["active"] = False
    return menu_config


def view_from_url(named_url):  # noqa
    """
    Finds and returns the view class from a named url
    """
    # code below is `stolen` from django's reverse method.
    resolver = get_resolver(get_urlconf())

    if type(named_url) in (list, tuple):
        named_url = named_url[0]
    parts = named_url.split(":")
    parts.reverse()
    view = parts[0]
    path = parts[1:]
    current_path = None
    resolved_path = []
    ns_pattern = ""
    ns_converters = {}

    # if it's a local url permission already given, so we just return true
    if named_url.startswith("#"):

        class LocalUrlDummyView:
            @staticmethod
            def has_permission(user):
                return True

        return LocalUrlDummyView

    while path:
        ns = path.pop()
        current_ns = current_path.pop() if current_path else None

        # Lookup the name to see if it could be an app identifier
        try:
            app_list = resolver.app_dict[ns]
            # Yes! Path part matches an app in the current Resolver
            if current_ns and current_ns in app_list:
                # If we are reversing for a particular app,
                # use that namespace
                ns = current_ns
            elif ns not in app_list:
                # The name isn't shared by one of the instances
                # (i.e., the default) so just pick the first instance
                # as the default.
                ns = app_list[0]
        except KeyError:
            pass

        if ns != current_ns:
            current_path = None

        try:
            extra, resolver = resolver.namespace_dict[ns]
            resolved_path.append(ns)
            ns_pattern = ns_pattern + extra
            try:
                ns_converters.update(resolver.pattern.converters)
            except Exception:
                pass
        except KeyError as key:
            if resolved_path:
                raise NoReverseMatch(
                    "%s is not a registered namespace inside '%s'"
                    % (key, ":".join(resolved_path))
                )
            else:
                raise NoReverseMatch("%s is not a registered namespace" % key)
    if ns_pattern:
        try:
            resolver = get_ns_resolver(
                ns_pattern, resolver, tuple(ns_converters.items())
            )
        except Exception:
            resolver = get_ns_resolver(ns_pattern, resolver)

    # custom code, get view from reverse_dict
    reverse_dict = resolver.reverse_dict.dict()
    for key, url_obj in reverse_dict.items():
        if url_obj == reverse_dict[view] and key != view:
            module = importlib.import_module(key.__module__)
            return getattr(module, key.__name__)


def find_attribute(obj, value):
    """
    Finds the attribute connected to the last object when a chain of
    connected objects is given in a string separated with double underscores.
    For example when a model x has a foreign key to model y and model y has
    attribute a, findattr(x, 'y__a') will return the a attribute from the y
    model that exists in x.
    """
    if "__" in value:
        value_list = value.split("__")
        attr = get_attribute(obj, value_list[0])
        return find_attribute(attr, "__".join(value_list[1:]))
    return get_attribute(obj, value)


def get_attribute(obj, value):
    """
    Normally the result of list_items for listviews are a set of model objects.
    But when you want a GROUP_BY query (with 'values' method), than
    the result will be a dict. This method will help you find an item for
    either objects or dictionaries.
    """
    if type(obj) == dict:
        return dict.get(obj, value)
    else:
        return getattr(obj, value)


def find_field_meta(obj, value):
    """
    In a model, finds the attribute meta connected to the last object when
    a chain of  connected objects is given in a string separated with double
    underscores.
    """
    if "__" in value:
        value_list = value.split("__")
        child_obj = obj._meta.get_field(value_list[0]).rel.to
        return find_field_meta(child_obj, "__".join(value_list[1:]))
    return obj._meta.get_field(value)


def get_field_class(qs, field_name):
    """
    Given a queryset and a field name, it will return the field's class
    """
    try:
        return qs.model._meta.get_field(field_name).__class__.__name__
    # while annotating, it's possible that field does not exists.
    except FieldDoesNotExist:
        return None


def reverse_url(url, obj, fallback_field=None):
    """
    Reverses a named url, in addition to the standard django reverse, it also
    accepts a list of ('named url', 'field1', 'field2', ...) and will use the
    value of the supplied fields as arguments.
    When a fallback field is given it will use it as an argument if none other
    are given.
    """
    args = []
    if type(url) in (list, tuple):
        named_url = url[0]
        for arg in url[1:]:
            if type(obj) is dict:
                args.append(obj[arg])
            else:
                args.append(find_attribute(obj, arg))
    else:
        if url[0] in "#/":  # local url or a path, just return it
            return url
        named_url = url
        if obj and fallback_field:
            if type(obj) is dict:
                args = [obj[fallback_field]]
            else:
                args = [get_attribute(obj, fallback_field)]

    # Instead of giving NoReverseMatch exception it's more desirable,
    # for field_links in listviews to just ignore the link.
    if fallback_field and not args:
        return ""

    return reverse(named_url, args=args)


def arctic_setting(setting_name, valid_options=None):
    """
    Tries to get a setting from the django settings, if not available defaults
    to the one defined in defaults.py
    """
    try:
        value = getattr(settings, setting_name)
        if valid_options and value not in valid_options:
            error_message = "Invalid value for {}, must be one of: {}".format(
                setting_name, str(valid_options)
            )
            raise ImproperlyConfigured(error_message)
    except AttributeError:
        pass
    return getattr(settings, setting_name, getattr(defaults, setting_name))


class RemoteDataSet:
    url_template = "?{filters}{fields}{order}{paginate}"
    paginate_template = "&offset={}&limit={}"
    order_separator = ","
    order_template = "&order={}"
    fields_separator = ","
    fields_template = "&fields={}"
    filters_template = "{}"
    filters_template_kv = "&{key}={value}"
    count = -1
    _options = {"fields": "", "order": "", "filters": "", "paginate": ""}
    page_size = None

    def fields(self, fields):
        if fields:
            fields_str = self.fields_separator.join(fields)
            self._options["fields"] = self.fields_template.format(fields_str)
        return deepcopy(self)

    def order_by(self, order):
        if order:
            order_str = self.order_separator.join(order)
            self._options["order"] = self.order_template.format(order_str)
        return deepcopy(self)

    def filter(self, **kwargs):
        if kwargs:
            filters = ""
            for key, value in kwargs.items():
                filters += self.filters_template_kv.format(
                    key=key, value=value
                )
            self._options["filters"] = self.filters_template.format(filters)
        return deepcopy(self)

    def get_url(self, start, stop):
        self._options["paginate"] = self.paginate_template.format(start, stop)
        url = self.url_template.format(**self._options)
        return url.replace("?&", "?")

    def get(self, start, stop):
        pass

    def __len__(self):
        return self.count

    def __getitem__(self, slice):
        return self.get(slice.start, slice.stop)


def offset_limit(func):
    """
    Decorator that converts python slicing to offset and limit
    """

    def func_wrapper(self, start, stop):
        offset = start
        limit = stop - start
        return func(self, offset, limit)

    return func_wrapper


def is_list_of_list(item):
    """
    check whether the item is list (tuple)
    and consist of list (tuple) elements
    """
    if (
        type(item) in (list, tuple)
        and len(item)
        and isinstance(item[0], (list, tuple))
    ):
        return True
    return False


def generate_id(*s):
    """
    generates an id from one or more given strings
    it uses english as the base language in case some strings
    are translated, this ensures consistent ids
    """
    with translation.override("en"):
        generated_id = slugify("-".join([str(i) for i in s]))
    return generated_id


def append_query_parameter(url, parameters, ignore_if_exists=True):
    """ quick and dirty appending of query parameters to a url """
    if ignore_if_exists:
        keys = list(parameters.keys())
        for key in keys:
            if key + "=" in url:
                del parameters[key]
    parameters_str = "&".join(k + "=" + v for k, v in parameters.items())
    append_token = "&" if "?" in url else "?"
    return url + append_token + parameters_str
