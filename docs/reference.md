# Settings Variables

## `ARCTIC_AUTOCOMPLETE`

Dictionary of models that when used as a foreign key should be lazy loaded when displayed in a form.
The dictionary has a key as slug, which will be used in the callback url,
and a list with the model path and the search field. For example:

    ARCTIC_AUTOCOMPLETE = {
        'authors': ('books.Author', 'name'),
    }

The callback url also needs to be setup in `urls.py`:

    urlpatterns = [
        ...
        url(r'^arctic/', include('arctic.urls', namespace='arctic')),
    ]

## `ARCTIC_COMMON_MEDIA_ASSETS`

Dictionary with JS/CSS resources, that has to be added to all pages. Note, the View has to be inherited from
`arctic.generics.View` to work. 
Example configuration is:

    ARCTIC_COMMON_MEDIA_ASSETS = {
        'css': {
            'all': ('common1.css', 'common2.css')
        },
        'js': ('common1.js', )
    }

## `ARCTIC_FORM_DISPLAY`

Defines how the forms should be displayed, options are:

- `float-field` - this is the default option, it shows a label in the form 
  field that 'floats' up when the field is filled.

- `stacked` - the labels are shown on top of the fields.

- `tabular` - the form will be displayed with labels next to the fields, this
  option does not support layouts.

## `ARCTIC_HIGHLIGHT_BACKGROUND`

String representing the highlight background color used in tags and other elements, if none given a default will be used.

## `ARCTIC_HIGHLIGHT_COLOR`

String representing the highlight foreground color used in tags and other elements, if none given a default will be used.

## `ARCTIC_INDEX_URL`
Name of the site index url. Default is "index". If no match found request redirect
to "/" happens.

## `ARCTIC_MENU`

Main menu that enables navigation between the different pages in Arctic.
It is a list with the format:

    (('menu label', 'named url', 'optional icon class', (optional submenu), (optional related url_names list)), ...)

## `ARCTIC_ROLES`

Dictionary of roles and their permissions, it uses the format:

    {'role1': ('permission1', 'permission2', ...), ...}

The 'admin' role is reserved and cannot be defined in settings. It gives full
rights to all views and can also be created with the `createsuperuser`
command.

## `ARCTIC_SIDEBAR_BACKGROUND`

String representing the background color of the sidebar, for example '#cccccc',
if not provided, a default color will be used.

## `ARCTIC_SIDEBAR_COLOR`

String representing the foreground color of the sidebar, for example '#ffffff',
if not provided, a default color will be used.

## `ARCTIC_SITE_LOGO`

The url of the logo to be displayed on every page, it will also be the link to
the homepage.

## `ARCTIC_SITE_NAME`

Name of the site.

## `ARCTIC_SITE_TITLE`

Title of the site to be used in the title tag. If not set it will use
`ARCTIC_SITE_NAME`

## `ARCTIC_PAGINATION`

Default pagination settings for `arctic_paginate` templatetag. 
All params should be defined in case overriding default settings. 

    ARCTIC_PAGINATION = {
        'show_label': True,
        'show_first_last': True,
        'range': 5,
    }


## `ARCTIC_PAGINATION_TEMPLATE`

Default pagination template used by `arctic_paginate` templatetag. 
Should be overridden in case customization pagination.

    ARCTIC_PAGINATION_TEMPLATE = 'arctic/partials/pagination.html'

## `LOGIN_URL` and `LOGOUT_URL`
Being a pure Django settings, LOGIN_URL and LOGOUT_URL used in Arctic to display
login and logout links. Both items supposed to be names of URLs. Defaults are 'login'
and 'logout'. Could be set to `None` if you don't want to use authentication in your app.

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

### `Media`

optional inner class indicating extra media assets to be included. If View is instance of FormView, 
or CreateView/UpdateView generics all assets defined in form used in the view will be also included. 

Example:

    from arctic.generics import View

    class MyView(View):
        class Media:
            css = {
                'all': ('extra.css',)
            }
            js = ('extra.js', 'another.js')

For more information on the Media class usage check the [Django Form Assets documentation](https://docs.djangoproject.com/en/dev/topics/forms/media/)

### `get_media_assets`
adds media assets dynamically to view. Does not overrides media from `Media` class but allows to set additional assets 
 on the fly.

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
* `arctic.mixins.ListMixin`
* `django.views.generic.ListView`

**Properties**

### `fields`

list of fields that should be displayed in the table, it is possible to
customize the field name by using a `(name, verbose_name)` tuple in the list
instead of a string.
Accessing fields from related objects is possible by using a double underscore
notation, for example if a model `book` has a foreign key to a model author
with a field name, `author__name` will display the field.

It's also possible to add virtual fields. See virtual fields for more info.

### `virtual fields`

Via the fields property, it's possible to add virtual fields. So you can
extend the views with custom fields. A virtual field does need an
accompanying method written like "get_{}_field". That method receives a
row_instance, so you can manipulate row data there.

Example:

    class MyListView(arctic.ListView):
        fields = (model_field1, model_field2, not_a_model_field)

        def get_not_a_model_field_field(row_instance):
            return '<b>' + row_instance.model_field3 + '</b>'

### `search_fields`

list of fields that are to be searched.

### `ordering_fields`

list of fields that can be ordered by clicking on the field's header column.


### `virtual ordering fields`

Via the fields property, it's possible to add virtual ordering fields. 
This is very userfull if we need to order by one of virtual field. For this 
you should extend the view with custom ordering fields. A virtual ordering field 
does need an accompanying method written like "get_{}_ordering_field". 

Example:

    class MyListView(arctic.ListView):
        fields = (model_field1, model_field2, not_a_model)
        ordering_fields = (model_field1, model_field2, not_a_model)
        
        def get_not_a_model_field(row_instance):
            return row_instance.created_at_UTC or row_instance.created_at_CET
        
        def get_not_a_model_ordering_field():
            return 'created_at_UTC'

### `sorting_field`

setting this property with a numberic database field will enable drag and drop 
sorting of rows in a `ListView`. Arctic urls need to be included for the 
callback urls; in the project's urls.py ensure the following is present:

    urlpatterns = [
        ...
        url(r'^arctic/', include('arctic.urls', namespace='arctic')),
    ]

When `sorting_field` is set, the following properties cannot be used: 
`ordering_fields`, `search_fields`, `default_ordering`, `advanced_search_form_class`
or `paginate_by`.

### `default_ordering`

list with default ordering of the fields, descending order uses Django's
standard notation by prepending a minus to the field, for example `-name`.

### `action_links`

optional list of `('name', 'base_url', 'optional icon class')` links, that
appear on the last column of the table and can apply a certain action, such
as delete.

### `get_field_actions(row)`

optional method to specify `action_links` per each row.
This method should return action links in same format, as `action_links` has. 
All returned actions, that are not defined in `action_links` field will be ignored.
Suggested approach is to remove actions from `action_links` copy, 
not preferred for current row:

    def get_field_actions(self, obj):
        actions = self.action_links.copy()
    
        if obj.is_published:
            actions = filter(lambda a: a != ('delete', 'staticpages:delete', 'fa-trash'), actions)
        else:
            actions = filter(lambda a: a != ('deactivate', 'staticpages:deactivate', 'fa-power-off'), actions)
    
        return actions


### `field_links`

dictionary of `{'field': 'base_url', ...}` that creates a link on the
content of the specified field that can apply a certain action, like edit.
By default the field link will use the current row id to create a link together 
with the `base_url`, if needed, the `base_url` can be given as a list or tuple where the first parameter is the named url followed by one or more field names, 
these field names can use the double underscore notation to access related 
objects, for example: `('category:list', 'category__slug')` 

### `field_classes`

dictionary of `{'field': 'css class', ...}` that adds an extra class to the specified field's cell, this enables the usage of client side widgets that
can transform the field data into a graphic representation.

### `get_{}_field_classes(row_instance)`
optional method to specify field classes per each row instance. 
Should return string of css classes `'css class'`.

Example:
```
    class MyListView(arctic.ListView):
        fields = {'online': ''}

        def get_online_field_classes(row_instance):
            if row_instance.published:
                return 'online'
            else:
                return 'offline'
```

### `tool_links`

This field contains links not connected to any individual table rows.
It is a list of tupples containing 2 items and an optional third.
The first item is the title of the link, and the second is a named url.

The optional third parameter can be a string with an icon (if no icon is 
provided the link will display the given title)
It is also possible to pass a dictionary as the third item, all of its keys will
be passed through to the template, the standard template recognizes the keys: 
`icon`, `style` (`link`, `primary`, `secondary` is default) and
`id` (by default auto generated from the english version of the title).

The maximum number of `tool_links` displayed is defined in `tool_links_collapse`,
whenever this number is reached, the remaining tool_links are displayed in a
dropdown.

Example:

    tool_links = (
        ('Add Arcticle', 'articles:create', 'fa-plus'),
    )

## `tool_links_collapse`

A number defining how many `tool_links` are to be displayed, any extra items 
will be available in a dropdown.

### `tool_links_icon`

This icon is used in the `tool_links` dropdown, by default an ellipsis `...`
will be used.

### `modals`

Dictionary of named urls that will be displayed in a modal.
Currently only the `confirm` type is supported. 
The format for this type is:

    {    
        'named_url': {
            'type': 'confirm',
            'title': 'Delete "{field_name}"',
            'message': 'Would you like to delete this?', 
            'ok': 'Delete', 
            'cancel': 'Cancel',
            'class': 'this_modal_class', # optional 
        },
        ...
    }

Both `title` and `message` can contain field names wrapped as python template
variables, which will be parsed into the field value for the row instance.
Currently `modals` work with `action_links` and `field_links`.
 
Confirm dialogs can be automatically picked up if a view includes the following method:

    @staticmethod 
    def confirm_dialog():
        return {
            'title': 'Delete "{field_name}"',
            'message': 'Would you like to delete this?',
            'ok': 'Delete',
            'cancel': 'Cancel',
            'class': 'this_dialog_class', # optional 
        }

The `obj` variable references the string representation of the object. Other 
individual fields present in the object can be used with the string template 
markup.

The use of the dialog can be disabled by return None in the confirm_dialog, if one already exists in the parent class.

### `simple_search_form_class`

By default Arctic uses `SimpleSearchForm` to be able search by `search_fields`.
Also this form supports `Quick filters` it like a buttons when you click on it, filter will be applied. It's useful when
you want to perform custom Q() query for each filter button.
Use `filters_select_multiple` variable to define which type of filters will be used. When you want select more than one active filter set `True`.

Example:

    class ExampleListView(ListView):
        ...
        advanced_search_form_class = QuickSearchForm
        ...


    from django.db.models import Q

    class QuickSearchForm(QuickFiltersFormMixin, SimpleSearchForm):
        filters_query_name = 'my_filters'
        filters_select_multiple = True
        FILTER_BUTTONS = (
            ('published', 'Is published'),
            ('rabbit', 'Find rabbit')
        )

        def get_search_filter(self):
            q = super(FiltersAndSearchForm, self).get_search_filter()

            values = self.cleaned_data.get(self.filters_query_name)
            conditions = {
                'published': Q(published=True),
                'rabbit': Q(description__icontains='rabbit')
            }

            for value in values:
                q |= conditions.get(value, Q())
            return q

### `advanced_search_form_class`

arctic provides a search endpoint via `advanced_search_form_class` which accepts a regular `django.forms.Form`.
A basic implementation of an advanced search form must implement the `get_search_filter()`.
Example:

    class ExampleListView(ListView):
        ...
        advanced_search_form_class = AdvancedSearchForm
        ...
    .
    .
    from django.db.models import Q

    class AdvancedSearchForm(Form):
        """
        Basic implementation of arctic's advanced search form class
        """
        modified_on = forms.DateTimeField(required=False,
                                          widget=forms.DateInput(attrs={'js-datepicker': ''}))
        created_on = forms.DateTimeField(required=False,
                                          widget=forms.DateInput(attrs={'js-datepicker': ''}))
                                      
        def get_search_filter(self):
            conditions = Q()
            modified_on_value = self.cleaned_data.get('modified_on')
            if modified_on_value:
                conditions &= Q(modified_on__gte=modified_on_value)
            created_on_value = self.cleaned_data.get('created_on')
            if created_on_value:
                conditions &= Q(created_on__gte=created_on_value)
            return conditions


## DataListView

`class arctic.generics.DataListView`

This view is similar in features to ListView but displays tabular data from an 
API source instead of a django model, it includes a default template and is 
able to do filtering, sorting, pagination and linking.
The biggest difference here is that DataListView requires a RemoteDataSet 
instance instead of a model.

A `RemoteDataSet` is a `QuerySet`-like object that acts as a gateway between 
the `DataListView` and an API at the very least it needs to implement the 
following:

- `url_template` property with optional `{filters}`, `{fields}`, `{order}` or
  `{paginate}` format paramenters, which in turn can be customized with their 
  own templates.

- `get()` method which accepts two parameters, by default `start` and `stop` or,
if using the `offset_limit` decorator then `offset` and `limit`. This method is
responsible to connect to the API with the `url_template` and fetch the data
needed to populate the list.

Example:

    from arctic.utils import RemoteDataSet, offset_limit

    class CountriesDataSet(RemoteDataSet):
        url_template = 'http://example.com/countries-api/?{filters}{fields}{order}{paginate}'
        order_template = '&order_by={}'

        @offset_limit
        def get(self, offset, limit):
            r = urllib.request.urlopen((self.get_url(offset, limit)))
            data = r.read().decode("utf-8")
            return json.loads(data)

    class CountryListView(DataListView):
        dataset = CountriesDataSet()
        ...

**Extends**

* `arctic.generics.TemplateView`
* `arctic.mixins.ListMixin`

**Properties**

### `fields`



## FormView

`class arctic.generics.FormView`

This view displays form data, it also includes a default template.

**Extends**

* `arctic.generics.View`
* `arctic.mixins.LayoutMixin`
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
* `arctic.mixins.LayoutMixin`
* `arctic.mixins.SuccessMessageMixin`
* `extra_views.CreateWithInlinesView`


## UpdateView

`class arctic.generics.UpdateView`

This view displays a form that updates data defined in a django model, it
includes a default template.

**Extends**

* `arctic.generics.View`
* `arctic.mixins.LayoutMixin`
* `arctic.mixins.SuccessMessageMixin`
* `extra_views.UpdateWithInlinesView`

**Properties**

### `readonly_fields`

List of strings of fieldnames that are rendered as readonly. Users cannot edit the input values,
but the value is displayed for reference.

## DeleteView

`class arctic.generics.DeleteView`

This view deletes data defined from a django model.

**Extends**

* `arctic.generics.View`
* `django.views.DeleteView`

**Properties**

### `redirect`

If `True` it will delete the object and imediately redirect to the success url 
not displaying the confirmation view.

**Methods**

### `get_success_message(obj)`

This method will return the success message to be displayed after the deletion 
of an object.

### `confirm_dialog()`

This static method will return the data needed to generate a confirmation 
dialog. Whenever this View is used in `action_links` or `field_links` in a `ListView`, a confirmation dialog will be displayed before the DeleteView is 
called.


# Mixins

## RoleAuthentication

`class arctic.mixins.RoleAuthentication`

This class provides role based authentication to a View. It is also used as a
standalone class to query other views about permissions and to synchronize the
roles defined in settings with the database instances.

**Properties**

### `permission_required`

This property defines which permissions should be checked when trying to access 
the view. When object based permission is needed, a method can be created
in the View with a matching name as the required permission. This method should
return a `True` if the permission is accepted or `False` if rejected.

It's either possible to define the permission as string, or as a list of 
strings - when checking on multiple permissions.

The property is mandatory by concept (when `login_required` is `False`),
so you have to define it when creating new Views.

The strings describing the permission can be anything, but it's advisable to 
follow Django's conventions, by using `<view|add|change|delete>_<entity>`
whenever it makes sense, for example `permission_required = 'view_user'`.


**Methods**

### `sync()`

This class method synchronizes the roles defined in the settings with the ones
in the database, this is needed to create relationships between Users and Roles.
This method is called every time arctic is started up.

### `has_permission()`

Checks if a user has the rights to access the current view. This is done firstly
by checking if the role the user has contains the defined `permission_required`
and secondly if a method with a name matching `permission_required` exists it
will check if it returns `True` or `False`. Note that on multiple
permissions, only one permission is needed to validate a user's role.


## FormMixin

`class arctic.mixins.RoleAuthentication`

This class provides common behaviours for `CreateView`, `UpdateView` and 
`FormView`

**Properties**

### `form_display`

Defines how a form will be displayed, the options are:

- `float-field` - this is the default option, it shows a label in the form 
  field that 'floats' up when the field is filled.

- `stacked` - the labels are shown on top of the fields.

- `tabular` - the form will be displayed with labels next to the fields, this
  option does not support layouts.

This option can be changed globally with the setting `ARCTIC_FORM_DISPLAY`.

### `layout`

List of fields to be displayed in a 12-column grid system.
By default a field will expand to full width, 12 columns.
It is possible to specify how many columns a field should use with the
`'field|n'` syntax where `n` can be a number from 1 to 12.
Fields can also be grouped into a single row by wrapping a list around them - 
`('field1', 'field2', 'field3')` if no amount of columns is given then these
fields will be evenly sized to fill up the entire row.

Fieldsets are also supported giving `layout` a dictionary where each key 
is the fieldset name and the values a field list. A fieldset can have an 
optional description by using the `'fieldset|description'` syntax.
When a fieldset name is prepended with a `-`, it will be collapsible and 
displayed as collapsed, if prepended with a `+` it will be collapsible and 
displayed as uncollapsed.

Examples:

    from collections import OrderedDict

    # category and tags on the same row, no fieldsets
    layout = ['title', 
              'description', 
              ['category', 'tags'], 
              'published', 
              'updated_at']

    # Two collapsible fieldsets, the first collapsed by default
    layout = OrderedDict([
        ('-fieldset', 
            ['title|10', 
            ['category', 'updated_at|4']]),                
        ('+fieldset2', 
            ['tags']),
        ])
    

    layout = [['published', 'updated_at']]

### `actions`

This field is used to add a number of links and buttons to the form.
It is a list of tupples containing 2 items and an optional third.
The first item is the title of the action, and the second is either a named url,
`submit` or `cancel`. 

The third parameter can be a string with the positioning of the action - the 
accepted value is `left` (right is the default).
It is also possible to pass a dictionary as the third item, all of its keys will
be passed through to the template, the standard template recognizes the keys: 
`position` (`left`), `style` (`link`, `primary`, `secondary` is default) and
`id` (by default auto generated from the english version of the title).

Example:

    actions = [
         ('Back to List', 'articles:list', 'left'),
         ('Cancel', 'cancel'), 
         ('Save as draft', 'submit'),
         ('Save', 'submit'),
    ]


# Apps

## users

Defines views and forms for easy user management. Lives under `arctic.users` directory.
By default provides `Create` and `Update` forms with following fields:

* username field(the field, defined as `USERNAME_FIELD` attribute)
* email
* is_active

You can override this behaviour with `FIELDS_CREATE` and `FIELDS_UPDATE` fields in your user model.

Example of custom user model:

    from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
    from django.db import models


    class User(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(unique=True)

        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)

        REQUIRED_FIELDS = ['password']
        USERNAME_FIELD = 'email'

        FIELDS_CREATE = ['email', 'is_active']
        FIELDS_UPDATE = ['is_active']
        ...

You can simply use built-in views:

    from arctic.users.views import (UserCreateView, UserListView, UserUpdateView)
    from django.conf.urls import url, include

    user_patterns = [
        include([
            url(r'^$', UserListView.as_view(), name='list'),
            url(r'^create/$', UserCreateView.as_view(), name='create'),
            url(r'^(?P<email>\w+)/$', UserUpdateView.as_view(), name='detail'),
        ], namespace='users')
    ]

Or inherit your classes to overwrite default behaviour and links. Please not that if you want to use
built-in views you need to define their urls under `users` namespace.

