# Overview

Django Arctic is a framework that simplifies the creation of custom content management systems.
It also includes a collection of optional components for common use cases, and
its core infrastructure is implementation agnostic.


##Why

There are a lot of content management systems in the market that are a good fit for the implementation of many web sites. Most CMS systems make assumptions about the data model for posts, authentication and the administration interface.

There is however a tipping point, where the need to customize a CMS product
is extensive enough that it ends up creating a more complex implementation than
if the product was developed directly with a generic framework. This is
specially true when the core of a CMS needs to be changed.

This is the case that Arctic wants to solve, creation of a CMS with a high degree of customization. Instead of being a ready-to-use CMS, Arctic is a framework that facilitates the construction of content management systems.


## Compatibility

* Python 2.7, 3.4, 3.5
* Django 1.8, 1.9


## Features

* Configurable menu
* Default responsive UI
* Role based authentication with permissions that can be object based.
* Optional tabbed interface to visually link multiple Views.
* ListViews support nested fields, sorting, filtering and linking.
* Forms with default improved widgets for datetime and option fields.


## Installation

Arctic is available on PIP:

    pip install django-arctic #TODO

or directly from Github:

    pip install git+ssh://git@github.com:sanoma/django-arctic.git


## Getting Started

Create a new Django project:

    django-admin startproject arctic_project

Change the settings.py:

In `TEMPLATES` - `OPTIONS` - `context_processors` add:

    'django.template.context_processors.request'

Add `'arctic'` to `INSTALLED_APPS`

Setup the menu:

    ARCTIC_MENU = (
        ('menu label', 'named url', 'optional icon class', (optional submenu)),
        ('menu label2', 'named url2', 'optional icon class2', (optional submenu2)),
        ...
    )


Set the site name and logo:

    ARCTIC_SITE_NAME = 'Arctic Project'
    ARCTIC_SITE_LOGO = '/path/to/logo.png'


Within the Arctic project there's an `example` project with a more extensive usage of Arctic's features.