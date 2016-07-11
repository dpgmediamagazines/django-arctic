from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from .models import UserRole
from .forms import UserCreationMultiForm

from arctic.generics import (
    ListView, UpdateView, CreateView,
    DeleteView, FormView)


class UserListView(ListView):
    paginate_by = 20
    model = UserRole
    fields = [('user__username', 'Username'), 'role__name', 'user__is_active',
              'user__last_login']
    ordering_fields = ['user__username']
    search_fields = ['user__username']
    # action_links = [
    #     ('delete', 'users:delete', 'fa-trash'),
    # ]
    field_links = {
        'user__username': 'users:detail',
    }
    tool_links = [
        (_('Create Users'), 'users:create'),
    ]

class UserCreateView(FormView):
    form_class = UserCreationMultiForm

class UserUpdateView(FormView):
    form_class = UserCreationMultiForm