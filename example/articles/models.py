# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals

from django.db import models


class Article(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    title = models.CharField("Title", max_length=255, null=False)
    description = models.TextField("Description", blank=True, null=False)
    published = models.BooleanField("Published", default=False)
    category = models.ForeignKey('articles.Category', verbose_name="Category")
    tags = models.ManyToManyField('articles.Tag')

    def __str__(self):
        return 'Article "' + self.title + '"'


class Category(models.Model):
    name = models.CharField('Name', max_length=255, null=False, blank=False,
                            unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    term = models.CharField('Term', max_length=255, null=False, blank=False,
                            unique=True)

    def __str__(self):
        return self.term
