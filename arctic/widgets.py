from django.forms.widgets import (DateInput, DateTimeInput, Select,
                                  SelectMultiple, TimeInput)


class Selectize(Select):
    def __init__(self, attrs, choices):
        super(Selectize, self).__init__(attrs, choices)
        attrs['js-selectize'] = True


class SelectizeMultiple(SelectMultiple):
    def __init__(self, attrs, choices):
        super(SelectizeMultiple, self).__init__(attrs, choices)
        attrs['js-selectize-multiple'] = True


class SelectizeAutoComplete(Select):
    def __init__(self, attrs, choices, url):
        super(SelectizeMultiple, self).__init__(attrs, choices)
        attrs['js-selectize-autocomplete'] = True
        attrs['data-url'] = url


class DateTimePickerInput(DateTimeInput):
    pass


class DatePickerInput(DateInput):
    pass


class TimePickerInput(TimeInput):
    pass
