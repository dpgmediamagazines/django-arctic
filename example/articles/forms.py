from __future__ import (absolute_import, unicode_literals)

from arctic.forms import SimpleSearchForm, QuickFiltersFormMixin
from django import forms
from django.db.models import Q

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'description', 'category', 'updated_at', 'tags',
                  'published']
        model = Article

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = ""


class AdvancedArticleSearchForm(forms.Form):
    description = forms.CharField(max_length=100,
                                  required=False,
                                  label='Description')

    def __init__(self, data):
        # Reset data, but store for get_search_filter
        self.stored_data = data
        super(AdvancedArticleSearchForm, self).__init__(data)

    def get_search_filter(self):
        value = self.cleaned_data.get('description')
        if value:
            return Q(description__icontains=value)
        return Q()


class FiltersAndSearchForm(QuickFiltersFormMixin, SimpleSearchForm):
    filters_query_name = 'my_filters'
    filters_select_multiple = True

    FILTER_BUTTONS = (
        ('published', 'Is published'),
        ('rabbit', 'Find rabbit')
    )

    def get_search_filter(self):
        q = super(FiltersAndSearchForm, self).get_search_filter()

        values = self.cleaned_data.get(self.filters_query_name)
        conditions = {
            'published': Q(published=True),
            'rabbit': Q(description__icontains='rabbit')
        }

        for value in values:
            q |= conditions.get(value, Q())

        return q
