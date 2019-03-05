# -*-*- encoding: utf-8 -*-*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    title = models.CharField(_("Title"), max_length=255, null=False)
    description = models.TextField(_("Description"), blank=True, null=False)
    published = models.BooleanField(_("Published"), default=False)
    category = models.ForeignKey(
        "articles.Category",
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField("articles.Tag")
    order = models.IntegerField(_("Order"), blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]


class Category(models.Model):
    name = models.CharField(
        _("Name"), max_length=255, null=False, blank=False, unique=True
    )
    order = models.IntegerField(_("Order"), blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    term = models.CharField(
        _("Term"), max_length=255, null=False, blank=False, unique=True
    )

    def __str__(self):
        return self.term


def filename(instance, filename):
    return "uploads/" + datetime.now().strftime("%Y%m%d%H%M%S%f") + ".jpg"


class Image(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=filename, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField("articles.Tag")
    updated = models.DateTimeField(null=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.title
