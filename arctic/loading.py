from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_role_model():
    """
    Returns the Role model that is active in this project.
    """
    app_model = getattr(
        settings,
        'ARCTIC_ROLE_MODEL',
        'arctic.Role'
    )

    try:
        return django_apps.get_model(app_model)
    except ValueError:
        raise ImproperlyConfigured("ARCTIC_ROLE_MODEL must be of the "
                                   "form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "ARCTIC_ROLE_MODEL refers to model '%s' that has not been "
            "installed" % settings.ARCTIC_ROLE_MODEL
        )


def get_user_role_model():
    """
    Returns the UserRole model that is active in this project.
    """
    app_model = getattr(
        settings,
        'ARCTIC_USER_ROLE_MODEL',
        'arctic.UserRole'
    )

    try:
        return django_apps.get_model(app_model)
    except ValueError:
        raise ImproperlyConfigured("ARCTIC_USER_ROLE_MODEL must be of the "
                                   "form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "ARCTIC_USER_ROLE_MODEL refers to model '%s' that has not been "
            "installed" % settings.ARCTIC_USER_ROLE_MODEL
        )
