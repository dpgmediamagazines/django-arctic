from datetime import datetime

import django
from django.forms.widgets import (
    ClearableFileInput,
    DateInput,
    DateTimeInput,
    Select,
    SelectMultiple,
    TextInput,
    TimeInput,
    Input,
    CheckboxSelectMultiple,
    RadioSelect,
)
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class StyledSelect(Select):
    def render(self, name, value, attrs=None, renderer=None):
        try:
            select_render = super(StyledSelect, self).render(
                name, value, attrs, renderer
            )
        except TypeError:  # versions older than Django 1.11
            select_render = super(StyledSelect, self).render(
                name, value, attrs
            )

        return mark_safe(
            '<div class="styled-select">{}</div>'.format(select_render)
        )


class Selectize(Select):
    def __init__(self, attrs={}, choices=()):
        attrs["js-selectize"] = True
        super(Selectize, self).__init__(attrs, choices)


class SelectizeMultiple(SelectMultiple):
    def __init__(self, attrs={}, choices=()):
        attrs["js-selectize-multiple"] = True
        super(SelectizeMultiple, self).__init__(attrs, choices)


class SelectizeAutoComplete(Select):
    def __init__(self, url, attrs={}, choices=()):
        attrs["js-selectize-autocomplete"] = True
        attrs["data-url"] = url
        super(SelectizeAutoComplete, self).__init__(attrs, choices)


class PickerFormatMixin(Input):
    """
    Handle formatting of widget input value

    Attributes:
        display_format(str): string that will
        be used to format input value before render

        widget_attribute_key(str): represents attribute name
        to which formatted input value will be assigned
    """

    display_format = None
    widget_attribute_key = None

    def get_context(self, name, value, attrs):
        context = super(PickerFormatMixin, self).get_context(
            name, value, attrs
        )
        if isinstance(value, datetime):
            value = value.strftime(self.display_format)
        context["widget"]["attrs"][self.widget_attribute_key] = value
        return context


class DateTimePickerInput(PickerFormatMixin, DateTimeInput):
    def __init__(self, attrs={}, format=None):
        attrs["js-datetimepicker"] = True
        self.display_format = "%m/%d/%Y %I:%M %p"
        self.widget_attribute_key = "data-datetime"
        super(DateTimePickerInput, self).__init__(attrs, format)


class DatePickerInput(PickerFormatMixin, DateInput):
    def __init__(self, attrs={}, format=None):
        attrs["js-datepicker"] = True
        self.display_format = "%m/%d/%Y"
        self.widget_attribute_key = "data-date"
        super(DatePickerInput, self).__init__(attrs, format)


class TimePickerInput(PickerFormatMixin, TimeInput):
    def __init__(self, attrs={}, format=None):
        attrs["js-timepicker"] = True
        self.display_format = "%I:%M %p"
        self.widget_attribute_key = "data-time"
        super(TimePickerInput, self).__init__(attrs, format)


class QuickFiltersSelectMixin(object):
    template_name = "arctic/widgets/quick_filters_select.html"

    def get_context(self, name, value, attrs=None, *args, **kwargs):
        if django.VERSION >= (1, 11):
            return super(QuickFiltersSelectMixin, self).get_context(
                name, value, attrs
            )
        else:
            # django 1.10 doesn't support optgroups
            # and render choices in method
            context = {"widget": self, "attrs": attrs}
            optgroups = []
            for val, label in self.choices:
                option = {
                    "name": name,
                    "value": val,
                    "selected": val in value,
                    "label": label,
                }
                optgroups.append((None, [option], None))
            context["widget"].optgroups = optgroups
        return context

    def render(self, name, value, attrs=None, renderer=None):
        """For django 1.10 compatibility"""
        if django.VERSION >= (1, 11):
            return super(QuickFiltersSelectMixin, self).render(
                name, value, attrs
            )

        t = render_to_string(
            template_name=self.template_name,
            context=self.get_context(name, value, attrs),
        )
        return mark_safe(t)


class QuickFiltersSelect(QuickFiltersSelectMixin, RadioSelect):
    """
    This widget is used when you want select only one active filter
    """


class QuickFiltersSelectMultiple(
    QuickFiltersSelectMixin, CheckboxSelectMultiple
):
    """
    This widget is used to be able to have a more than one active filters
    """

    def __init__(self, attrs=None, **kwargs):
        attrs = attrs or {}
        attrs["select_multiple"] = True
        super().__init__(attrs, **kwargs)


class SearchInput(TextInput):
    """
    Widget used in the inline search field on top of ListViews
    """

    template_name = "arctic/widgets/search_input.html"

    def render(self, name, value, attrs=None, renderer=None):
        """For django 1.10 compatibility"""
        if django.VERSION >= (1, 11):
            return super(SearchInput, self).render(name, value, attrs)

        t = render_to_string(
            template_name=self.template_name,
            context=self.get_context(name, value, attrs),
        )
        return mark_safe(t)


class BetterFileInput(ClearableFileInput):
    """
    File input replacement with Image preview
    """

    template_name = "arctic/widgets/file_input.html"

    def render(self, name, value, attrs=None, renderer=None):
        """For django 1.10 compatibility"""
        if django.VERSION >= (1, 11):
            return super(BetterFileInput, self).render(name, value, attrs)

        t = render_to_string(
            template_name=self.template_name,
            context=self.get_context(name, value, attrs),
        )
        return mark_safe(t)
