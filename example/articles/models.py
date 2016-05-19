# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals

from django.db import models

class Article(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField("Title", max_length=255, null=False)
    description = models.TextField("Description", blank=True, null=False)
    published = models.BooleanField(default=False)
    image = models.ForeignKey('images.Image', null=True, blank=True)
    category = models.ForeignKey('articles.Category', null=True, blank=True)
    tags = models.ManyToManyField('articles.Tag')


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)


class Tag(models.Model):
    term = models.CharField(max_length=255, null=False, blank=False, unique=True)