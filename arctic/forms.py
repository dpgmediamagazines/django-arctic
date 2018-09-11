import operator

from arctic.widgets import SearchInput
from django import forms
from functools import reduce

from django.db.models import Q


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=50, widget=SearchInput, required=False)

    def __init__(self, search_fields=[], *args, **kwargs):
        super(SimpleSearchForm, self).__init__(*args, **kwargs)
        self.search_fields = search_fields

    def get_search_filter(self):
        value = self.data.get("search")
        if not value:
            return Q()

        q_list = []
        for field_name in self.search_fields:
            q_list.append(Q(**{field_name + "__icontains": value}))

        return reduce(operator.or_, q_list)
