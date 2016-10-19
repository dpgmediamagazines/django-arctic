"""
Basic mixins for generic class based views.
"""

from __future__ import (absolute_import, unicode_literals)

from arctic.utils import view_from_url
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import (ImproperlyConfigured, PermissionDenied)
from django.utils import six

from arctic.loading import (get_role_model, get_user_role_model)

Role = get_role_model()
UserRole = get_user_role_model()


class SuccessMessageMixin(object):
    """
    Adds a success message on successful form submission.
    Altered to work with extra_views
    """
    success_message = ''

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def forms_valid(self, form, inlines):
        response = super(SuccessMessageMixin, self).forms_valid(form, inlines)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            object=self.object,
        )


class LinksMixin(object):
    """
    Adding links to view, to be resolved with 'arctic_url' template tag
    """
    def get_links(self):
        if not self.links:
            return None
        else:
            allowed_links = []
            for link in self.links:

                # check permission based on named_url
                if not view_from_url(link[1]).has_permission(self.request.user):
                    continue

                allowed_links.append(link)
            return allowed_links


class RoleAuthentication(object):
    """
    This class adds a role relation to the standard django auth user to add
    support for role based permissions in any class - usually a View.
    """
    ADMIN = 'admin'
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request.user):
            raise PermissionDenied()
        return super(RoleAuthentication, self).dispatch(request, *args, **kwargs)

    @classmethod
    def sync(cls):
        """
        Save all the roles defined in the settings that are not yet in the db
        this is needed to create a foreign key relation between a user and a
        role. Roles that are no longer specified in settings are set as
        inactive.
        """

        try:
            settings_roles = set(settings.ARCTIC_ROLES.keys())
        except AttributeError:
            settings_roles = set()

        saved_roles = set(Role.objects.values_list('name', flat=True))
        unsaved_roles = settings_roles - saved_roles
        unused_roles = saved_roles - settings_roles - set([cls.ADMIN])

        # ensure that admin is not defined in settings
        if cls.ADMIN in settings_roles:
            raise ImproperlyConfigured('"' + cls.ADMIN + '" role is reserved '
                                       'and cannot be defined in settings')

        # ensure that admin exists in the database
        if cls.ADMIN not in saved_roles:
            Role(name=cls.ADMIN, is_active=True).save()

        # check if the role defined in settings already exists in the database
        # and if it does ensure it is enabled.
        for role in saved_roles:
            if role in settings_roles:
                saved_role = Role.objects.get(name=role)
                if not saved_role.is_active:
                    saved_role.is_active = True
                    saved_role.save()

        for role in unsaved_roles:
            Role(name=role).save()

        for role in unused_roles:
            unused_role = Role.objects.get(name=role)
            unused_role.is_active = False
            unused_role.save()

    @classmethod
    def get_permission_required(cls):
        """
        Get permission required property.
        Must return an iterable.
        """

        if cls.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(cls.__name__)
            )
        if isinstance(cls.permission_required, six.string_types):
            perms = (cls.permission_required,) if cls.permission_required != "" else ()
        else:
            perms = cls.permission_required

        return perms

    @classmethod
    def has_permission(cls, user):
        """
        We override this method to customize the way permissions are checked.
        Using our roles to check permissions.
        """
        # no login is needed, so its always fine
        if not cls.requires_login:
            return True

        # if user is somehow not logged in
        if not user.is_authenticated():
            return False

        # attribute permission_required is mandatory, returns tuple
        perms = cls.get_permission_required()
        # if perms are defined and empty, we skip checking
        if not perms:
            return True

        # get role of user, skip admin role
        role = UserRole.objects.get(user=user).role.name
        if role == cls.ADMIN:
            return True

        # check if at least one permissions is valid
        for permission in perms:
            if cls.check_permission(role, permission):
                return True

        # permission denied
        return False

    @classmethod
    def check_permission(cls, role, permission):
        """
        Check if role contains permission
        """
        result = permission in settings.ARCTIC_ROLES[role]
        # will try to call a method with the same name as the permission
        # to enable an object level permission check.
        if result:
            try:
                return getattr(cls, permission)(role)
            except AttributeError:
                pass
        return result
