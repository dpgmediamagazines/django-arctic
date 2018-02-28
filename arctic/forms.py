import operator
from django import forms
from functools import reduce

from django.db.models import Q

from arctic.widgets import QuickFiltersSelect


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)

    def __init__(self, search_fields=[], *args, **kwargs):
        super(SimpleSearchForm, self).__init__(*args, **kwargs)
        self.search_fields = search_fields

    def get_search_filter(self):
        value = self.data.get('search')
        if not value:
            return Q()

        q_list = []
        for field_name in self.search_fields:
            q_list.append(Q(**{field_name + '__icontains': value}))

        return reduce(operator.or_, q_list)


class QuickFiltersForm(forms.Form):
    filters_field_name = 'quick_filters'

    def __init__(self, request=None, *args, **kwargs):
        super(QuickFiltersForm, self).__init__(*args, **kwargs)

        if not hasattr(self, 'FILTER_BUTTONS'):
            raise AttributeError(
                'QuickFiltersForm '
                'must contains FILTER_BUTTONS list')
        self.fields[self.filters_field_name] = forms.ChoiceField(
            required=False,
            choices=self.FILTER_BUTTONS,
            widget=QuickFiltersSelect(attrs={'request': request}),
            label=''
        )

    def get_current_filter(self):
        return self.cleaned_data[self.filters_field_name]
