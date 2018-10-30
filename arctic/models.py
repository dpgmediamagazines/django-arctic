from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserRole(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="urole",
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey("arctic.Role", on_delete=models.CASCADE)

    class Meta:
        swappable = "ARCTIC_USER_ROLE_MODEL"
        ordering = ["user"]


class Role(models.Model):
    name = models.CharField(_("Role"), max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        swappable = "ARCTIC_ROLE_MODEL"
        ordering = ["name"]
