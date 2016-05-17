# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals

from django.db import models


class Image(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    caption = models.CharField(max_length=255, null=False)
    tags = models.CharField(max_length=255, null=False)
    url = models.ImageField()
