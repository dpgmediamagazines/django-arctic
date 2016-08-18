from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from arctic.models import (Role, UserRole)

from .mixins import RoleAuthentication

User = get_user_model()


def superuser_post_save(sender, instance, **kwargs):
    if instance.is_superuser:
        RoleAuthentication.sync()
        admin = Role.objects.get(name='admin')
        try:
            UserRole.objects.get(user=instance, role=admin)
        except UserRole.DoesNotExist:
            UserRole(user=instance, role=admin).save()

post_save.connect(superuser_post_save, sender=User)
