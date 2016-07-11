from collections import OrderedDict

from django import forms
from django.contrib.auth import get_user_model

from betterforms.multiform import MultiModelForm
from .models import UserRole

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active',)


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ('role',)


class UserCreationMultiForm(MultiModelForm):
    form_classes = OrderedDict([
        ('user', UserForm),
        ('role', UserRoleForm),
    ])
