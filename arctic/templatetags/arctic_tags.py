from __future__ import unicode_literals, absolute_import
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


# TODO Cleanup this file. Lot unnused


@register.simple_tag(takes_context=True)
def update_plugin_groups_counter(context):
    context['plugin_groups_counter'] += 1
    return ''


@register.filter()
def empty_plugin_form(formset, plugin_type):
    return formset.empty_plugin_form(plugin_type)


@register.filter()
def verbose_name(model):
    return model._meta.verbose_name


@register.filter()
def verbose_name_plural(model):
    return model._meta.verbose_name_plural


def get_parameters(parser, token):
    """
    {% get_parameters except_field %}
    """

    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            "get_parameters tag takes at least 1 argument")
    return GetParametersNode(args[1].strip())


class GetParametersNode(template.Node):
    """
    Renders current get parameters except for the specified parameter
    """
    def __init__(self, field):
        self.field = field

    def render(self, context):
        request = context['request']
        getvars = request.GET.copy()

        if self.field in getvars:
            del getvars[self.field]

        if len(getvars.keys()) > 0:
            get_params = "%s&" % getvars.urlencode()
        else:
            get_params = ''

        return get_params


get_parameters = register.tag(get_parameters)


def get_all_fields(obj):
    """Returns a list of all field names on the instance."""
    fields = []
    for f in obj._meta.fields:
        fname = f.name

        get_choice = 'get_' + fname + '_display'
        if hasattr(obj, get_choice):
            value = getattr(obj, get_choice)()
        else:
            try:
                value = getattr(obj, fname)
            except:
                value = None

        if isinstance(value, list):
            value = ','.join(str(v) for v in value)

        if f.editable and value and f.name:

            fields.append({
                'label': f.verbose_name,
                'name': f.name,
                'value': value})

    return fields


@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    ''' Add param to the given query string '''
    params = context['request'].GET.copy()

    for key, value in list(kwargs.items()):
        params[key] = value

    return '?' + params.urlencode()


@register.simple_tag(takes_context=True)
def query_string_ordering(context, value, **kwargs):
    """
    Add ordering param to the given query string
    :param context: template context
    :param value: examples would be '-id' or 'id'. A minus indicates that the default sorting is descending
    :param kwargs: not used
    :return: Adjusted query string, starting with '?'
    """
    params = context['request'].GET.copy()

    # if the given value is '-id', it's core value would be 'id'
    core_value = value
    default_order = 'asc'

    if core_value[0] == '-':
        core_value = value[1:]
        default_order = 'desc'

    current_value = ''

    # by preference get the current ordering value from the filter
    # so that even if no explicit ordering is in the URL, we still
    # get the implicit ordering, the page's default
    # See generics.filters.FilterSet
    if 'filter' in context:
        current_value = context['filter'].ordered_value()
    elif 'ordering' in params:
        current_value = params['ordering']

    # The first two clauses check if the current ordering is on the
    # same field as the desired one, in which case we reverse the direction.
    # If it's on another field, we use the default direction.
    if current_value == core_value:
        order_prefix = '-'
    elif current_value == '-' + core_value:
        order_prefix = ''
    elif default_order == 'desc':
        order_prefix = '-'
    else:
        order_prefix = ''

    params['ordering'] = order_prefix + core_value
    return '?' + params.urlencode()


@register.simple_tag(takes_context=True)
def arctic_url(context, link, *args, **kwargs):
    """
    Resolves display- and tool-link tuples into urls with optional
    item IDs and parent IDs. See base_list.html for example usage.

    We could tie this to check_url_access() to check for permissions,
    including object-level.
    """
    url_args = args

    if 'parent_ids' in context:
        if args and context['parent_ids']:
            url_args = context['parent_ids'] + args
        elif context['parent_ids']:
            url_args = context['parent_ids']

    return reverse(link, args=url_args, kwargs=None)


class SubViewNode(template.Node):

    def __init__(self, view):
        self.view = template.Variable(view)

    def render(self, context):
        view = self.view.resolve(context)
        view.request = context['request']
        view.args = []
        view.kwargs = {}

        return view.render(context['parent_ids'][-1])


@register.tag
def subview(parser, token):
    args = token.split_contents()
    if len(args) != 2:
        raise template.TemplateSyntaxError(
            "subview tag takes one argument")
    return SubViewNode(args[1])


@register.filter()
def lookup(dct, key):
    return dct.get(key)

@register.filter()
def typename(obj):
    return type(obj).__name__


@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
