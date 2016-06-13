# -*-*- encoding: utf-8 -*-*-
# pylint: disable=E1101
from __future__ import unicode_literals, absolute_import
import operator
from functools import reduce

from django import forms
from django.db.models import DateTimeField, Q
import django_filters
from django_filters.widgets import RangeWidget


class SearchInput(forms.TextInput):
    """ Normal text input with search flag.
    Just so the frontend knows it's a search box
    """
    is_search = True


class DateRangeInput(RangeWidget):
    """ Range widget used for range date input.
    Just so the frontend knows it's a date range box
    """
    pass


class FilterSet(django_filters.FilterSet):
    filter_overrides = {
        DateTimeField: {
            'filter_class': django_filters.DateFromToRangeFilter,
            'extra': lambda f: {
                'widget': DateRangeInput,
            }
        }
    }
    search_fields = None

    def __init__(self, *args, **kwargs):
        super(FilterSet, self).__init__(*args, **kwargs)
        for filter_name in self.filters:
            """ We want a descriptive title for selects """
            if isinstance(self.filters[filter_name],
                          django_filters.ModelChoiceFilter):
                self.filters[filter_name].extra.update(
                    {'empty_label': u"%s" % self.filters[filter_name].label}
                )
            elif isinstance(self.filters[filter_name],
                            django_filters.ChoiceFilter):
                choices = (('', self.filters[filter_name].label),) + \
                          self.filters[filter_name].extra['choices']
                self.filters[filter_name].extra.update(
                    {'choices': choices}
                )

    def search_filter(self, queryset, value):
        if self.search_fields:
            q_list = []
            for field_name in self.search_fields:
                q_list.append(Q(**{field_name + '__icontains': value}))

            queryset = queryset.filter(reduce(operator.or_, q_list))

        return queryset


def filterset_factory(model, fields, search_fields=None):
    if search_fields:
        fields = list(fields) + ['search']

    class DynamicFilterSet(FilterSet):
        if search_fields:
            search = django_filters.MethodFilter(action='search_filter',
                                                 widget=SearchInput)

    meta = type(str('Meta'), (object,), {
        'model': model,
        'fields': fields,
    })
    filterset = type(
        str('%sFilterSet' % model._meta.object_name), (DynamicFilterSet,), {
            'Meta': meta,
            'search_fields': search_fields,
        }
    )

    return filterset
