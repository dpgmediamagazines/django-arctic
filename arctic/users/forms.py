from collections import OrderedDict

from django import forms
from django.contrib.auth import forms as user_forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from betterforms.multiform import MultiModelForm

from arctic.loading import get_user_role_model

User = get_user_model()
UserRole = get_user_role_model()


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ('role',)


class UserCreationForm(user_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active',)


class UserCreationMultiForm(MultiModelForm):
    form_classes = OrderedDict([
        ('user', UserCreationForm),
        ('role', UserRoleForm),
    ])

    def save(self, commit=True):
        objects = super(UserCreationMultiForm, self).save(commit=False)

        if commit:
            user = objects['user']
            user.save()
            user_role = objects['role']
            user_role.user = user
            user_role.save()

        return objects


class UserChangeForm(forms.ModelForm):
    new_password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Leave this field empty if you don't want to change your "
                    "password."),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'is_active',)

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)

        new_password = self.cleaned_data["new_password"]
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class UserChangeMultiForm(MultiModelForm):
    form_classes = OrderedDict([
        ('user', UserChangeForm),
        ('role', UserRoleForm),
    ])
