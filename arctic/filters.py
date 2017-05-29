from __future__ import (absolute_import, unicode_literals)

import operator
from functools import reduce

from django import forms
from django.db.models import (DateTimeField, Q, BooleanField)

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


class BooleanFilterSelect(forms.NullBooleanSelect):
    """ Yes/No select widget for boolean select field. """
    def render(self, name, value, attrs=None):
        for option_value, option_label in enumerate(self.choices):
            if option_label[0] == '1':
                self.choices[option_value] = (option_label[0], name)
            else:
                label = name + ': ' + str(option_label[1])
                self.choices[option_value] = (option_label[0], label)

        return super(BooleanFilterSelect, self).render(name, value, attrs)


class FilterSet(django_filters.FilterSet):

    class Meta:
        filter_overrides = {
            DateTimeField: {
                'filter_class': django_filters.DateFromToRangeFilter,
                'extra': lambda f: {
                    'widget': DateRangeInput,
                }
            },
            BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': BooleanFilterSelect,
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
                    tuple(self.filters[filter_name].extra['choices'])
                self.filters[filter_name].extra.update(
                    {'choices': choices}
                )

    def search_filter(self, queryset, name, value):
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
            search = django_filters.CharFilter(method='search_filter',
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
