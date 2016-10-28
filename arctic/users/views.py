from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from arctic.models import UserRole, Role
from .forms import UserCreationMultiForm, UserChangeMultiForm

from arctic.generics import (
    ListView, UpdateView, CreateView,
    DeleteView, FormView)

User = get_user_model()
username_field = User.USERNAME_FIELD


class UserListView(ListView):
    page_title = _('Users')
    paginate_by = 20
    model = UserRole
    fields = [('user__{}'.format(username_field), 'Username'), 'role__name', 'user__is_active',
              'user__last_login']
    ordering_fields = ['user__{}'.format(username_field), 'role__name', 'user__last_login']
    search_fields = ['user__{}'.format(username_field)]
    filter_fields = ['user__is_active']
    # action_links = [
    #     ('delete', 'users:delete', 'fa-trash'),
    # ]
    field_links = {
        'user__{}'.format(username_field): 'users:detail',
    }
    tool_links = [
        (_('Create Users'), 'users:create', 'fa-plus'),
    ]


class UserCreateView(CreateView):
    page_title = _('Create User')
    model = UserRole
    success_url = reverse_lazy('users:list')
    form_class = UserCreationMultiForm

    def get_success_message(self, cleaned_data):
        return _('User {} was successfully created').format(self.object['user'])


class UserUpdateView(UpdateView):
    page_title = _('Change User')
    model = UserRole
    success_url = reverse_lazy('users:list')
    form_class = UserChangeMultiForm

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object.user,
            'role': self.object
        })
        return kwargs

    def get_success_message(self, cleaned_data):
        return _('User {} was successfully updated').format(self.object['user'])
