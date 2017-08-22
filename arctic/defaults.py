# options are 'float-label', 'stacked' or 'tabular'
ARCTIC_FORM_DISPLAY = 'float-label'

ARCTIC_SITE_LOGO = 'arctic/dist/assets/img/arctic_logo.svg'

ARCTIC_SITE_NAME = 'Arctic Site Name'

ARCTIC_WIDGET_OVERLOADS = {
    'DateInput': 'arctic.widgets.DatePickerInput',
    'DateTimeInput': 'arctic.widgets.DateTimePickerInput',
    'TimeInput': 'arctic.widgets.TimePickerInput',
    'Select': 'arctic.widgets.StyledSelect',
    'SelectMultiple': 'arctic.widgets.SelectizeMultiple',
    'MultipleChoiceField': 'arctic.widgets.Selectize',
}
