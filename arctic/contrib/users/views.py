from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from .models import UserRole

from arctic.generics import (
    ListView, UpdateView, CreateView,
    DeleteView)

#User = get_user_model()

class UserListView(ListView):
    paginate_by = 20
    model = UserRole
    fields = [('user__username', 'Username'), 'role__name', 'user__is_active', 'user__last_login']
    ordering_fields = ['user__username']
    search_fields = ['user__username']
    # action_links = [
    #     ('delete', 'articles:delete'),
    # ]
    # field_links = {
    #     'title': 'articles:detail',
    #     'published': 'articles:detail',
    # }
    # field_classes = {
    #     'published': 'inline-widget boolean-circle',
    # }
    # tool_links = [
    #     (_('Create Article'), 'articles:create'),
    # ]
    # required_permission = "articles_view"
