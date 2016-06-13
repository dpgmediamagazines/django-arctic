from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from arctic.generics import (
    ListView, UpdateView, CreateView,
    DeleteView, TemplateView)


class LoginView(TemplateView):
    template_name = 'arctic/login.html'
    page_title = "Login"
    requires_login = False
    messages = []

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LoginView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')
        context['messages'] = set(self.messages)
        return context

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            login(request, user)
        else:
            self.messages.append('Invalid username/password combination')

        return redirect(request.GET.get('next', '/'))
