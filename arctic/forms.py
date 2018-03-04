import operator

from arctic.widgets import QuickFiltersSelect
from django import forms
from functools import reduce

from django.db.models import Q


class SimpleSearchForm(forms.Form):
    filters_query_name = None
    FILTER_BUTTONS = ()

    search = forms.CharField(max_length=100, required=False)

    def __init__(self, search_fields=[], *args, **kwargs):
        super(SimpleSearchForm, self).__init__(*args, **kwargs)
        self.search_fields = search_fields

        if self.filters_query_name:
            self.fields[self.filters_query_name] = forms.ChoiceField(
                required=False,
                choices=self.FILTER_BUTTONS,
                widget=QuickFiltersSelect
            )

    def get_search_filter(self):
        value = self.data.get('search')
        filter_query = self.get_quick_filter_query()
        if not value:
            return Q() & filter_query

        q_list = []
        for field_name in self.search_fields:
            q_list.append(Q(**{field_name + '__icontains': value}))

        return reduce(operator.or_, q_list) & filter_query

    def get_quick_filter_query(self):
        """Returns Q () conditions in depends for filter query"""
        if self.filters_query_name:
            raise NotImplementedError(
                'For using quick_filters you must implement '
                '"get_quick_filter_query()" in the simple_search_form_class'
            )
        else:
            return Q()

    def get_quick_filters_field(self):
        """Dynamically render form field in template"""
        return self[self.filters_query_name]
