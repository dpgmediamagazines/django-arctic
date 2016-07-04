from django.apps import AppConfig

class ArcticConfig(AppConfig):
    name = 'arctic'

    # even though db usage in AppConfig is not a recommended best practice
    # according to the Django docs, this is the best location to sync the
    # roles defined in settings.ARCTIC_ROLES to the database.
    def ready(self):
        from .mixins import RoleAuthentication
        try:
            RoleAuthentication.sync()
        except:
            pass