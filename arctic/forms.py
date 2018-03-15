import operator

from arctic.widgets import QuickFiltersSelect, QuickFiltersSelectMultiple
from django import forms
from functools import reduce

from django.db.models import Q


class QuickFiltersFormMixin(object):
    filters_query_name = None
    filters_select_multiple = True
    FILTER_BUTTONS = ()

    def __init__(self, *args, **kwargs):
        super(QuickFiltersFormMixin, self).__init__(*args, **kwargs)

        if self.filters_query_name:
            self.fields[self.filters_query_name] = self._filter_form_field(
                required=False,
                choices=self.FILTER_BUTTONS,
                widget=self._filter_field_widget(
                    attrs={'select_multiple': self.filters_select_multiple}
                )
            )

    def get_quick_filters_field(self):
        """Dynamically render form field in template"""
        return self[self.filters_query_name]

    @property
    def _filter_form_field(self):
        """Return form form field according to multiple select possibility"""
        if self.filters_select_multiple:
            return forms.MultipleChoiceField
        else:
            return forms.ChoiceField

    @property
    def _filter_field_widget(self):
        """Return field widget according to multiple select possibility"""
        if self.filters_select_multiple:
            return QuickFiltersSelectMultiple
        else:
            return QuickFiltersSelect


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
