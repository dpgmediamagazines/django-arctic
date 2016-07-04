# -*-*- encoding: utf-8 -*-*-
"""
Basic mixins for generic class based views.
"""

from __future__ import unicode_literals, absolute_import

from django.contrib import messages
#from django.contrib.auth.models import Group
from django.conf import settings

from .contrib.users.models import Role

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
                allowed_links.append(link)
            return allowed_links


class RoleAuthentication():
    """
    This class (mis)uses the groups concept from django auth to add role
    based permissions support to any class.
    """
    required_permission = None

    @classmethod
    def sync(cls):
        """
        Save all the roles defined in the settings that are not yet in the db
        this is needed to create a foreign key relation between a user and a
        group.
        """
        saved_roles = set(Role.objects.values_list('name', flat=True))
        unsaved_roles = set(settings.ARCTIC_ROLES.keys()) - saved_roles
        unused_roles = saved_roles - set(settings.ARCTIC_ROLES.keys())

        for role in unsaved_roles:
            Role(name=role).save()
        for role in unused_roles:
            unused = Role.objects.get(name=role)
            unused.is_active = False
            unused.save()


    def assign_role(self, role, user):
        group = Group.objects.get(name=role)
        user.groups.clear() # users only have one role
        user.groups.add(group)

    def revoke_role(self, role, user):
        user.groups.clear()

    def has_perm(self, user):
        if user.is_superuser or (not self.required_permission):
            return True
        role = user.groups.all()[0].name # there is only one group per user
        result = self.required_permission in settings.ARCTIC_ROLES[role]
        # will try to call a method with the same name as the permission
        # to enable an object level permission check.
        if result:
            try:
                return getattr(self, self.required_permission)(role)
            except AttributeError:
                pass
        return result
