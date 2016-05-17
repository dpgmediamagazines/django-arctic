# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals

from django.db import models

class Article(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField("Title", max_length=255, null=False)
    description = models.TextField("Description", blank=True, null=False)
    published = models.BooleanField(default=False)
    tags = models.CharField(max_length=255, null=False)
    image = models.ForeignKey('images.Image', null=True, blank=True)
