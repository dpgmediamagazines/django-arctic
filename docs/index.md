# Overview

Django Arctic is a framework built on top of Django that facilitates the creation of custom Dashboards, Admin Interfaces or Content Management Systems in an quick and DRY way.


## Features

* Does not depend on any models
* Optional Authentication/Permission system
* Class based views that match and extend the ones from Django
* Default User Interface which can be customised or replaced.


## Installation

Arctic is available on PIP:

    pip install django-arctic #TODO

or directly from Github:

    pip install git+https://github.com/sanoma/django-arctic.git#egg=django-arctic


## Getting Started

Create a new Django project:

    django-admin startproject arctic_project

Change the settings.py:

In `TEMPLATES` - `OPTIONS` - `context_processors` add:

    'django.template.context_processors.request'

Add `'arctic'` to `INSTALLED_APPS`




