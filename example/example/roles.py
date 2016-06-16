from django.contrib.auth.models import Group

user.groups.add(group)


class RoleManager():
    roles = ['admin', 'reader']
    permissions = []

    def __init__(self):
        """
        Save all the roles defined in the class that are not yet in the db
        """
        saved_roles = Group.objects.values_list('name', flat=True))
        unsaved_roles = set(self.roles).difference()

        for role in unsaved_roles:
            self.add_role(role)

    def add_role(self, role):
        group = Group(name=role).save()

    def add_user_to_role(self, role, user):
        group = Group.objects.get(name=role)
        user.groups.add(group)

