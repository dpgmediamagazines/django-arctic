# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals, absolute_import

from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'description', 'category', 'published']
        model = Article
