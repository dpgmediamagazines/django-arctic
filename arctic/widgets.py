from django.forms.widgets import (DateInput, DateTimeInput, Select,
                                  SelectMultiple, TimeInput)


class Selectize(Select):
    pass


class SelectizeMultiple(SelectMultiple):
    pass


class SelectizeAutoComplete(Select):
    pass


class DateTimePickerInput(DateTimeInput):
    pass


class DatePickerInput(DateInput):
    pass


class TimePickerInput(TimeInput):
    pass
