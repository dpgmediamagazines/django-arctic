# Authentication and Roles

Arctic uses the underlying Django authentication backend, but it adds its own
role base permission system. It also includes a user management app.

## Creating an admin user

When Arctic is installed, the Django `createsuperuser` command will create a 
User that is also setup with the `admin` role in Arctic, this role has full 
access to every view in Arctic:

    ./manage.py createsuperuser

## Arctic `users` app

This app has a UI to manage users in arctic.

In `urls.py` add the following to `urlpatterns`:

    urlpatterns = [
        ...
        url(r'^users/', include('arctic.users.urls', namespace='users')),
]

And in `settings.py` add a reference to `ARCTIC_MENU`:

    ARCTIC_MENU = (
        ...
        ('Users', 'users:list', 'fa-user'),
    )


## Setting up permissions in Views

Every Arctic view needs a `permission_required` property, this property should 
be unique and will be used in the definition of roles. For example:

    permission_required = 'view_user'

The convention to be used here is the same as what django uses for its model 
based permissions: `<view|add|change|delete>_<entity>`


## Defining roles

Roles are defined in the settings with the `ARCTIC_ROLES` dictionary, the key 
of the dictionary is the role name, and its value is a list of permissions that
have been defined in the `premission_required` property of the Views, for
example:

    ARCTIC_ROLES = {
        'editor': ('view_user', 'view_article', 'add_article', 'change_article',)
        ...
    }




