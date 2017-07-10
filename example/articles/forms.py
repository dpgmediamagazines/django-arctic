from __future__ import (absolute_import, unicode_literals)

from django import forms

from .models import Article
from django.db.models import Q


class ArticleForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'description', 'category', 'updated_at', 'tags',
                  'published']
        model = Article

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = ""


class AdvancedCategorySearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label='Strict name match')

    def get_search_filter(self):
        value = self.data.get('name')
        if value:
            return Q(name=value)
        return Q()