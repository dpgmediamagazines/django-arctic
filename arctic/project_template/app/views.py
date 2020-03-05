from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from arctic.generics import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import {{ camel_case_app_name }}Form
from .models import {{ camel_case_app_name }}


class {{ camel_case_app_name }}ListView(ListView):
    model = {{ camel_case_app_name }}
    fields = '__all__'
    permission_required = 'view_{{ app_name }}'

    # Delete and detail action link
    action_links = [
        ("detail", "{{ app_name}}:detail", "fa-edit"),
        ("delete", "{{ app_name}}:delete", "fa-trash"),
    ]

    # tool link to create
    tool_links = [
        (_("Create {{ app_name }}"), "{{ app_name }}:create", "fa-plus"),
    ]

    # Some optional fields
    # paginate_by = 10
    # ordering_fields = ['field_name1', ..]
    # search_fields = ['field_name', ...]
    # allowed_exports = ["csv"]


class {{ camel_case_app_name }}CreateView(CreateView):
    model = {{ camel_case_app_name }}
    form_class = {{ camel_case_app_name }}Form
    permission_required = 'add_{{ app_name }}'

    def get_success_url(self):
        return reverse("{{app_name}}:detail", args=(self.object.pk,))


class {{ camel_case_app_name }}UpdateView(UpdateView):
    model = {{ camel_case_app_name }}
    form_class = {{ camel_case_app_name }}Form
    permission_required = 'change_{{ app_name }}'
    success_url = reverse_lazy('{{app_name}}:list')
    actions = [
        (_("Cancel"), "cancel"),
        (_("Save"), "submit"),
    ]


class {{ camel_case_app_name }}DeleteView(DeleteView):
    model = {{ camel_case_app_name }}
    success_url = reverse_lazy('{{app_name}}:list')
    permission_required = 'delete_{{ app_name }}'
