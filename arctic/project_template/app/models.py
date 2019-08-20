# -*-*- encoding: utf-8 -*-*-

from django.db import models


class {{ camel_case_app_name }}(models.Model):
    # Add DB fields

    # Optional add name
    def __str__(self):
        # return self.name
