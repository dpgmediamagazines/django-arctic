from django import forms
from django.db.models import Q
from django.http import HttpRequest
from django.template import Context, Template
from bs4 import BeautifulSoup

from arctic.forms import SimpleSearchForm
from arctic.widgets import QuickFiltersSelect


class FiltersForm(SimpleSearchForm):
    FILTER_BUTTONS = (
        ('published', 'Is published'),
        ('find_rabbit', 'Rabbit')
    )

    quick_filters = forms.ChoiceField(
        choices=FILTER_BUTTONS,
        widget=QuickFiltersSelect
    )

    def get_search_filter(self):
        quick_filter = self.cleaned_data.get('quick_filters')

        if quick_filter == 'published':
            return Q(published=True)
        if quick_filter == 'find_rabbit':
            return Q(description__icontains='rabbit')
        return Q()


def test_simple_search_form():
    data = {'search': None}
    search_fields = ['name']

    form = SimpleSearchForm(search_fields=search_fields, data=data)
    search_filter = form.get_search_filter()

    # Empty search value, should return empty filter
    assert str(search_filter) == str(Q())

    data = {'search': 'test'}
    form = SimpleSearchForm(search_fields=search_fields, data=data)
    search_filter = form.get_search_filter()

    # Filled in search value, should return icontains filter
    assert str(search_filter) == str(Q(('name__icontains', 'test')))


def test_filters_widget_attr():
    widget = QuickFiltersSelect

    assert hasattr(widget, 'widget_type')
    assert widget.widget_type == 'quick_filter'
    assert widget.input_type == 'hidden'
    assert widget.template_name == 'arctic/widgets/quick_filters_select.html'


def test_form_rendering_with_request_get_args():
    request = HttpRequest()
    request.GET['search'] = 'cats'
    request.GET['quick_filters'] = 'published'

    form = FiltersForm(data=request.GET)
    assert form.is_valid()

    template = Template('{{ form }}').render(Context({"form": form}))

    soup = BeautifulSoup(template, 'html.parser')

    filters_inputs = soup.find_all('input', {'type': 'radio'})
    filters_buttons = soup.find_all('button')

    assert len(filters_inputs) == len(form.FILTER_BUTTONS)
    assert len(filters_buttons) == len(form.FILTER_BUTTONS)

    for inp, btn, choice in zip(
            filters_inputs,
            filters_buttons,
            form.FILTER_BUTTONS):
        assert btn.text.strip() == choice[1]
        assert btn['onclick'] == "select_quick_filter(this)"
        assert inp.get('hidden') == ''
        assert inp.get('value') == choice[0]
        assert inp.get('name') == 'quick_filters'

    # check if we marked selected filter
    assert filters_inputs[0].attrs.get('checked') == ''
