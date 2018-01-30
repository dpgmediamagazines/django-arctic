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


class AdvancedArticleSearchForm(forms.Form):
    description = forms.CharField(max_length=100,
                                  required=False,
                                  label='Description')

    def get_search_filter(self):
        value = self.cleaned_data.get('description')
        if value:
            return Q(description__icontains=value)
        return Q()
