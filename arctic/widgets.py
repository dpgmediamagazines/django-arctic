from datetime import datetime

from django.forms.widgets import (DateInput, DateTimeInput, Select,
                                  SelectMultiple, TimeInput, Input)
from django.utils.safestring import mark_safe


class StyledSelect(Select):
    def render(self, name, value, attrs=None, renderer=None):
        try:
            select_render = super(StyledSelect, self).render(
                name, value, attrs, renderer)
        except TypeError:  # versions older than Django 1.11
            select_render = super(StyledSelect, self).render(
                name, value, attrs)

        return mark_safe('<div class="styled-select">{}</div>'.format(
            select_render))


class Selectize(Select):
    def __init__(self, attrs, choices):
        attrs['js-selectize'] = True
        super(Selectize, self).__init__(attrs, choices)


class SelectizeMultiple(SelectMultiple):
    def __init__(self, attrs, choices):
        attrs['js-selectize-multiple'] = True
        super(SelectizeMultiple, self).__init__(attrs, choices)


class SelectizeAutoComplete(Select):
    def __init__(self, attrs, choices, url):
        attrs['js-selectize-autocomplete'] = True
        attrs['data-url'] = url
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
        if not value:
            value = datetime.now().strftime(self.display_format)
        elif isinstance(value, datetime):
            value = value.strftime(self.display_format)
        context['widget']['attrs'][self.widget_attribute_key] = value
        return context


class DateTimePickerInput(PickerFormatMixin, DateTimeInput):
    def __init__(self, attrs, format):
        attrs['js-datetimepicker'] = True
        self.display_format = '%m/%d/%Y %I:%M %p'
        self.widget_attribute_key = 'data-datetime'
        super(DateTimePickerInput, self).__init__(attrs, format)


class DatePickerInput(PickerFormatMixin, DateInput):
    def __init__(self, attrs, format):
        attrs['js-datepicker'] = True
        self.display_format = '%m/%d/%Y'
        self.widget_attribute_key = 'data-date'
        super(DatePickerInput, self).__init__(attrs, format)


class TimePickerInput(PickerFormatMixin, TimeInput):
    def __init__(self, attrs, format):
        attrs['js-timepicker'] = True
        self.display_format = '%I:%M %p'
        self.widget_attribute_key = 'data-time'
        super(TimePickerInput, self).__init__(attrs, format)
