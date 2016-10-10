# from django.db import models

# import pytest
# from mixer.backend.django import mixer
# pytestmark = pytest.mark.django_db


# class Book(models.Model):
#     title = models.CharField("Title", max_length=255, null=False)
#     description = models.TextField("Description", blank=True, null=False)
#     category = models.ForeignKey('tests.Category')
#     tags = models.ManyToManyField('tests.Tag')


# class Category(models.Model):
#     name = models.CharField('Name', max_length=255, null=False, blank=False,
#                             unique=True)

#     def __str__(self):
#         return self.name


# class Tag(models.Model):
#     name = models.CharField('Tag', max_length=255, null=False, blank=False,
#                             unique=True)

#     def __str__(self):
#         return self.name
