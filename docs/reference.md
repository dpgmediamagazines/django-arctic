# Settings Variables

## `ARCTIC_SITE_LOGO`

The url of the logo to be displayed on every page, it will also be the link to
the homepage.

## `ARCTIC_SITE_NAME`

Name of the site.

## `ARCTIC_SITE_TITLE`

Title of the site to be used in the title tag. If not set it will use
`ARCTIC_SITE_NAME`

## `ARCTIC_MENU`

Main menu that enables navigation between the different pages in Arctic.
It is a list with the format:

    (('menu label', 'named url', 'optional icon class', (optional submenu)), ...)

## `ARCTIC_ROLES`

Dictionary of roles and their permissions, it uses the format:

    {'role1': ('permission1', 'permission2', ...), ...}

The 'admin' role is reserved and cannot be defined in settings. It gives full
rights to all views and can also be created with the `createsuperuser`
command.

## `ARCTIC_TOPBAR_BACKGROUND_COLOR`

String representing the background color of the topbar, for example '#cccccc',
if not provided, a default color will be used.

## `ARCTIC_HIGHLIGHT_COLOR`

String representing the highlight color used in table headers, the side menu,
and tag item backgrounds, if none given a default will be used.


# Generic Class Based Views

Arctic provides a number of class based views that add integration with the
user interface and extra functionality for common use cases.
The class names match and work the same way as the ones that Django provides
and should be used instead.

## View

`class arctic.generics.View`

This view is used for all the views in Arctic, except the LoginView.

**Extends**

* `django.views.generic.View`
* `arctic.mixins.RoleAuthentication`

**Properties**

### `breadcrumbs`

list of `('name', 'url')` that represents a breadcrumb trail. The last item will
represent the current page and the url will be ignored, so `None` can be used
instead of an url.

### `page_title`

title to be displayed in title tag and page header.

### `page_description`

description of the current page.

### `tabs`

list of `('title', 'url')` tabs that relate the current views with other views,
one of the tuples should point to the current view.

### `requires_login`

indicates if this view can only be accessed by authenticated users.
Can be `True` or `False`, default is `True`.


**Methods**

### `get_site_logo()`

url path to the site logo, it will try to use `ARCTIC_SITE_LOGO` from the project settings, if none given a default image will be used.

### `get_site_name()`

site name, , it will try to use `ARCTIC_SITE_NAME` from the project settings, if none given a default name will be used.

### `get_site_title()`

site title to be used in the html `title` tag, it will try to use
`ARCTIC_SITE_TITLE` from the project settings, if none given it will fallback
to `ARCTIC_SITE_NAME`.

### `get_index_url()`

This represents the home url, and it's used as a link in the site logo.
By default will attempt to use the `index` named url, if it doesn't exist, will
return the `/` url path.


## TemplateView

`class arctic.generics.TemplateView`

This view extends the standard Django TemplateView and integrates it in the
Arctic user interface. There are no added methods or properties besides the
ones inherited by its ancestors.

**Extends**

* `arctic.generics.View`
* `django.views.generic.TemplateView`


## ListView

`class arctic.generics.ListView`

This view displays tabular data from a django model, it includes a default
template and is able to do filtering, sorting, pagination and linking.

**Extends**

* `arctic.generics.View`
* `django.views.generic.ListView`

**Properties**

### `fields`

list of fields that should be displayed in the table, it is possible to
customize the field name by using a `(name, verbose_name)` tuple in the list
instead of a string.
Accessing fields from related objects is possible by using a double underscore
notation, for example if a model `book` has a foreign key to a model author
with a field name, `author__name` will display the field.

### `search_fields`

list of fields that are to be searched.

### `ordering_fields`

list of fields that can be ordered by clicking on the field's header column.

### `default_ordering`

list with default ordering of the fields, descending order uses Django's
standard notation by prepending a minus to the field, for example `-name`.

### `action_links`

optional list of `('name', 'base_url', 'optional icon class')` links, that
appear on the last column of the table and can apply a certain action, such
as delete.

### `field_links`

dictionary of `{'field': 'base_url', ...}` that creates a link on the
content of the specified field that can apply a certain action, like edit.

### `field_classes`

dictionary of `{'field': 'css class', ...}` that adds an extra class to the specified field's cell, this enables the usage of client side widgets that
can transform the field data into a graphic representation.

### `tool_links`

list of links with the format `('name', 'url')`, not connected to the table data.


## FormView

`class arctic.generics.FormView`

This view displays form data, it also includes a default template.

**Extends**

* `arctic.generics.View`
* `arctic.mixins.SuccessMessageMixin`
* `django.views.FormView`


## DetailView

`class arctic.generics.DetailView`

This view displays data from a model using a default template.

**Extends**

* `arctic.generics.View`
* `arctic.mixins.LinksMixin`
* `django.views.DetailView`


## CreateView

`class arctic.generics.CreateView`

This view displays a form that creates data for a django model, it includes a
default template.

**Extends**

* `arctic.generics.View`
* `arctic.mixins.SuccessMessageMixin`
* `django.views.CreateView`


## UpdateView

`class arctic.generics.UpdateView`

This view displays a form that updates data defined in a django model, it
includes a default template.

**Extends**

* `arctic.generics.View`
* `arctic.mixins.SuccessMessageMixin`
* `django.views.UpdateView`


## DeleteView

`class arctic.generics.DeleteView`

This view deletes data defined from a django model.

**Extends**

* `arctic.generics.View`
* `arctic.mixins.SuccessMessageMixin`
* `django.views.DeleteView`


# Mixins

## RoleAuthentication

`class arctic.mixins.RoleAuthentication`

This class provides role based authentication to a View. It is also used as a
standalone class to query other views about permissions and to synchronize the
roles defined in settings with the database instances.

**Properties**

### `permission_required`

This property defines which permissions should be checked when trying to access 
the view. When object based permission is needed, an extra method can be created
in the View with a matching name as the required permission. This method should
return a `True` if the permission is accepted or `False` if rejected.


**Methods**

### `sync()`

This class method synchronizes the roles defined in the settings with the ones
in the database, this is needed to create relationships between Users and Roles.
This method is called every time arctic is started up.

### `has_perm()`

Checks if a user has the rights to access the current view. This is done firstly
by checking if the role the user has contains the defined `required_permission`
and secondly if a method with a name matching `required_permission` exists it
will check if it returns `True` or `False`.


# Apps

## users

TBD
