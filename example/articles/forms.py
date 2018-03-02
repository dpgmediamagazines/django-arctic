from __future__ import (absolute_import, unicode_literals)

from django import forms
from django.db.models import Q

from arctic.widgets import QuickFiltersSelect

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
    FILTER_BUTTONS = (
        ('published', 'Is published'),
        ('find_rabbit', 'Rabbit')
    )
    description = forms.CharField(max_length=100,
                                  required=False,
                                  label='Description')

    quick_filters = forms.ChoiceField(required=False, choices=FILTER_BUTTONS, widget=QuickFiltersSelect)

    def get_search_filter(self):
        value = self.cleaned_data.get('description')
        quick_filter = self.cleaned_data.get('quick_filters')
        conditions = Q()

        if value:
            conditions &= Q(description__icontains=value)
        if quick_filter == 'published':
            conditions &= Q(published=True)
        if quick_filter == 'find_rabbit':
            conditions &= Q(description__icontains='rabbit')
        return conditions
