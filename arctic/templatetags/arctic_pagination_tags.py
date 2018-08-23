# inspired and partially copied from
# https://github.com/jmcclell/django-bootstrap-pagination

import re

import django

from django.template import (
    Node,
    Library,
    TemplateSyntaxError,
    VariableDoesNotExist,
)
from django.template.loader import get_template

# As of django 1.10, template rendering no longer accepts a context, but
# instead accepts only accepts a dict. Up until django 1.8, a context was
# actually required. Fortunately Context takes a single dict parameter,
# so for django >=1.9 we can get away with just passing a unit function.
from arctic.utils import arctic_setting

if django.VERSION < (1, 9, 0):
    from django.template import Context
else:

    def Context(x):
        return x


register = Library()


def get_current_app(context):
    try:
        current_app = context.request.current_app
    except AttributeError:
        try:
            current_app = context.request.resolver_match.namespace
        except AttributeError:
            return None
    return current_app


def str_to_bool(val):
    """
    Helper function to turn a string representation of "true" into
    boolean True.
    """
    if isinstance(val, str):
        val = val.lower()

    return val in ["true", "on", "yes", True]


class PaginationNode(Node):
    """
    Render the pagination bar with the given parameters
    """

    def __init__(self, page, kwargs):
        self.page = page
        self.kwargs = kwargs

    def render(self, context):
        kwargs = {}

        # Retrieve variable instances from context where necessary
        for argname, argvalue in self.kwargs.items():
            try:
                kwargs[argname] = argvalue.resolve(context)
            except AttributeError:
                kwargs[argname] = argvalue
            except VariableDoesNotExist:
                kwargs[argname] = None

        # Unpack our keyword arguments, substituting defaults where necessary

        PAGINATION_SETTINGS = arctic_setting("ARCTIC_PAGINATION")

        show_label = str_to_bool(
            kwargs.get("show_label", PAGINATION_SETTINGS["show_label"])
        )
        show_first_last = str_to_bool(
            kwargs.get(
                "show_first_last", PAGINATION_SETTINGS["show_first_last"]
            )
        )
        range_length = kwargs.get("range", PAGINATION_SETTINGS["range"])
        if range_length is not None:
            range_length = int(range_length)

        # Generage our viewable page range
        page = self.page.resolve(context)
        paginator = kwargs.pop("paginator", None)

        page_count = paginator.num_pages if paginator else 1
        current_page = page.number if page else 1

        if page_count == -1:
            # assume total objects length is unknown, pages are not required
            show_first_last = False
            page_range = None
            first_page_index = None
            last_page_index = None
        else:
            if range_length is None:
                range_min = 1
                range_max = page_count
            else:
                if range_length < 1:
                    raise Exception(
                        'Optional argument "range" '
                        "expecting integer greater than 0"
                    )
                elif range_length > page_count:
                    range_length = page_count

                range_length -= 1
                range_min = max(current_page - (range_length // 2), 1)
                range_max = min(current_page + (range_length // 2), page_count)
                range_diff = range_max - range_min
                if range_diff < range_length:
                    shift = range_length - range_diff
                    if range_min - shift > 0:
                        range_min -= shift
                    else:
                        range_max += shift

            page_range = range(range_min, range_max + 1)

            first_page_index = 1
            last_page_index = page_count

        return get_template(
            arctic_setting("ARCTIC_PAGINATION_TEMPLATE")
        ).render(
            Context(
                {
                    "page_obj": page,
                    "paginator": paginator,
                    "request": context["request"],
                    "show_first_last": show_first_last,
                    "page_range": page_range,
                    "first_page_index": first_page_index,
                    "last_page_index": last_page_index,
                    "show_label": show_label,
                }
            )
        )


@register.tag
def arctic_paginate(parser, token):
    """
    Renders a Page object with pagination bar.
    Example::
        {% arctic_paginate page_obj paginator=page_obj.paginator range=10 %}
    Named Parameters::
        range - The size of the pagination bar (ie, if set to 10 then, at most,
                10 page numbers will display at any given time) Defaults to
                None, which shows all pages.
        show_first_last - Accepts "true" or "false". Determines whether or not
                          to show the first and last page links. Defaults to
                          "false"
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "'%s' takes at least one argument"
            " (Page object reference)" % bits[0]
        )
    page = parser.compile_filter(bits[1])
    kwargs = {}
    bits = bits[2:]

    kwarg_re = re.compile(r"(\w+)=(.+)")

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError(
                    "Malformed arguments to bootstrap_pagination paginate tag"
                )
            name, value = match.groups()
            kwargs[name] = parser.compile_filter(value)

    return PaginationNode(page, kwargs)
