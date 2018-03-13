from django.db.models import Q
from django.http import HttpRequest
from django.template import Context, Template
from bs4 import BeautifulSoup

from arctic.forms import SimpleSearchForm, QuickFiltersFormMixin
from arctic.widgets import QuickFiltersSelect, QuickFiltersSelectMultiple


class FiltersForm(QuickFiltersFormMixin, SimpleSearchForm):
    FILTER_BUTTONS = (
        ('published', 'Is published'),
        ('find_rabbit', 'Rabbit')
    )
    filters_query_name = 'my_filters'
    filters_select_multiple = True

    def get_quick_filter_query(self):
        value = self.cleaned_data.get(self.filters_query_name)

        if value == 'published':
            return Q(published=True)
        elif value == 'rabbit':
            return Q(description__icontains='rabbit')
        else:
            return Q()


class FiltersFormSelectOne(FiltersForm):
    filters_select_multiple = False


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
    assert widget.template_name == 'arctic/widgets/quick_filters_select.html'


def test_filters_form_field():
    form = FiltersForm()

    assert form.fields.get('my_filters')

    assert form.get_quick_filters_field().field == form.fields['my_filters']

    assert not form.fields['my_filters'].required
    assert not form.fields['my_filters'].choices == form.FILTER_BUTTONS


def test_filters_form_widget_selecting():
    form = FiltersForm()
    widget = form.fields['my_filters'].widget
    assert isinstance(widget, QuickFiltersSelectMultiple)

    form = FiltersFormSelectOne()
    widget = form.fields['my_filters'].widget
    assert isinstance(widget, QuickFiltersSelect)


def test_form_rendering_with_request_get_args():
    request = HttpRequest()
    request.GET['search'] = 'cats'
    request.GET['my_filters'] = 'published'

    form = FiltersForm(data=request.GET)
    assert form.is_valid()

    template = Template('{{ form }}').render(Context({"form": form}))

    soup = BeautifulSoup(template, 'html.parser')

    filters_inputs = soup.find_all('input', {'type': 'checkbox'})
    filters_buttons = soup.find_all('label', {'class': 'btn'})

    assert len(filters_inputs) == len(form.FILTER_BUTTONS)
    assert len(filters_buttons) == len(form.FILTER_BUTTONS)

    for inp, btn, choice in zip(
            filters_inputs,
            filters_buttons,
            form.FILTER_BUTTONS):
        assert btn.text.strip() == choice[1]
        assert inp.get('value') == choice[0]
        assert inp.get('name') == 'my_filters'

    # check if we marked selected filter
    assert filters_inputs[0].attrs.get('checked') == ''


def test_filters_form_rendering_select_one():
    request = HttpRequest()
    request.GET['search'] = 'cats'
    request.GET['my_filters'] = 'published'

    form = FiltersFormSelectOne(data=request.GET)
    assert form.is_valid()

    template = Template('{{ form }}').render(Context({"form": form}))

    soup = BeautifulSoup(template, 'html.parser')
    filters_inputs = soup.find_all('input', {'type': 'checkbox'})

    assert filters_inputs[0].attrs.get('checked') is None
