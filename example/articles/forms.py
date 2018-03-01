from __future__ import (absolute_import, unicode_literals)

from django import forms
from django.db.models import Q

from arctic.forms import QuickFiltersForm

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

    def get_search_filter(self):
        value = self.cleaned_data.get('description')
        if value:
            return Q(description__icontains=value)
        return Q()


class QuickArticleFiltersForm(QuickFiltersForm):
    FILTER_BUTTONS = (
        ('published', 'Is published'),
        ('find_rabbit', 'Rabbit')
    )

    def get_filters(self):
        f = self.get_current_filter()

        if f == 'published':
            return Q(published=True)
        if f == 'find_rabbit':
            return Q(description__icontains='rabbit')
        return Q()
