# options are 'float-label', 'stacked' or 'tabular'
ARCTIC_FORM_DISPLAY = "float-label"

ARCTIC_SITE_LOGO = "arctic/dist/assets/img/arctic_logo.svg"

ARCTIC_SITE_NAME = "Arctic Site Name"

ARCTIC_WIDGET_OVERLOADS = {
    "DateInput": "arctic.widgets.DatePickerInput",
    "DateTimeInput": "arctic.widgets.DateTimePickerInput",
    "ClearableFileInput": "arctic.widgets.BetterFileInput",
    "FileInput": "arctic.widgets.BetterFileInput",
    "TimeInput": "arctic.widgets.TimePickerInput",
    "Select": "arctic.widgets.StyledSelect",
    "SelectMultiple": "arctic.widgets.SelectizeMultiple",
    "MultipleChoiceField": "arctic.widgets.Selectize",
}

ARCTIC_PAGINATION = {"show_label": True, "show_first_last": True, "range": 5}

ARCTIC_PAGINATION_TEMPLATE = "arctic/partials/pagination.html"
