# Working with Lists

Arctic has `ListView`s that greatly extend the ones provided by Django, this 
tutorial will explore all its features.
It is recomended to use the project created in the [Getting Started](../#getting-started) chapter as a starting point.

## Database backed ListView

In this tutorial we're going to explore Arctic's ListView features, to start
we're going first create a new Django app, in the terminal go to your project's 
directory:

    ./manage.py startapp articles

Add `'articles'` to `INSTALLED_APPS` in `config/settings.py`

Then create a data model in `articles/models.py`:

    from django.db import models


    class Article(models.Model):
        created_at = models.DateTimeField(auto_now=True)
        title = models.CharField("Title", max_length=255, null=False)
        description = models.TextField("Description", blank=True, null=False)
        published = models.BooleanField("Published", default=False)
        category = models.ForeignKey('articles.Category', verbose_name="Category")

        class Meta:
            ordering = ['id']


    class Category(models.Model):
        name = models.CharField('Name', max_length=255, null=False, blank=False,
                                unique=True)


Back in the terminal setup the database with the newly created models:

    ./manage.py makemigrations
    ./manage.py migrate

The new models need to be populated so that the ListView can display something,
since there are no forms created yet, we'll just do it in the python shell:


    # install lorem to generate some dummy data
    pip install lorem
    ./manage.py shell

    >>> import lorem
    >>> from articles.models import Article, Category
    >>> categories = ['general', 'politics', 'sport', 'nature', 'international']
    >>> from random import choice, randint
    >>> for category in categories:
    ...     Category(name=category).save()
    >>>
    >>> for _ in range(30):
    ...     category_name = categories[randint(0, len(categories) - 1)]
    ...     category = Category.objects.get(name=category_name)
    ...     published = (randint(0, 2) == True)
    ...     Article(title=lorem.sentence(), description=lorem.paragraph(),
    ...             published=choice([True, False]), category=category).save()
    >>> exit()

At this point a data model has been created and populated with some random data,
so far this has been just standard Django.

Now with some data to display lets create a ListView in `articles.views.py`:

from arctic.generics import ListView



