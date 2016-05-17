# Overview

Django Arctic is a framework that simplifies the creation of custom content management systems.


## Features

* Does not depend on any models
* Optional Authentication/Permission system
* Class based views that match and extend the ones from Django
* Default User Interface which can be customised or replaced


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