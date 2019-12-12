from django import forms

from .models import {{ camel_case_app_name }}


class {{ camel_case_app_name }}Form(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = {{ camel_case_app_name }}
