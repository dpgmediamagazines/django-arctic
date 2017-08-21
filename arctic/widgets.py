from datetime import datetime

from django.forms.widgets import (DateInput, DateTimeInput, Select,
                                  SelectMultiple, TimeInput)
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


class DateTimePickerInput(DateTimeInput):
    def __init__(self, attrs, format):
        attrs['js-datetimepicker'] = True
        super(DateTimePickerInput, self).__init__(attrs, format)

    def get_context(self, name, value, attrs):
        context = super(DateTimePickerInput, self).get_context(name, value,
                                                               attrs)
        if not value:
            value = datetime.now()
        context['widget']['attrs']['data-datetime'] =\
            value.strftime('%m/%d/%Y %I:%M %p')
        return context


class DatePickerInput(DateInput):
    def __init__(self, attrs, format):
        attrs['js-datepicker'] = True
        super(DatePickerInput, self).__init__(attrs, format)

    def get_context(self, name, value, attrs):
        context = super(DatePickerInput, self).get_context(name, value, attrs)
        if not value:
            value = datetime.now()
        context['widget']['attrs']['data-date'] =\
            value.strftime('%m/%d/%Y')
        return context


class TimePickerInput(TimeInput):
    def __init__(self, attrs, format):
        attrs['js-timepicker'] = True
        super(TimePickerInput, self).__init__(attrs, format)

    def get_context(self, name, value, attrs):
        context = super(TimePickerInput, self).get_context(name, value, attrs)
        if not value:
            value = datetime.now()
        context['widget']['attrs']['data-time'] =\
            value.strftime('%I:%M %p')
        return context
