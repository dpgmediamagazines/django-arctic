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
    filters_query_name = 'my_filters'

    def get_quick_filter_query(self):
        value = self.cleaned_data.get(self.filters_query_name)

        if value == 'published':
            return Q(published=True)
        elif value == 'rabbit':
            return Q(description__icontains='rabbit')
        else:
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
    assert widget.template_name == 'arctic/widgets/quick_filters_select.html'


def test_filters_form_field():
    form = FiltersForm()

    assert form.fields.get('my_filters')

    widget = form.fields['my_filters'].widget
    assert isinstance(widget, QuickFiltersSelect)

    assert not form.fields['my_filters'].required
    assert not form.fields['my_filters'].choices == form.FILTER_BUTTONS


def test_filters_form_errors():
    class WrongFiltersForm(SimpleSearchForm):
        filters_query_name = 'some_name'

    form = WrongFiltersForm()

    try:
        form.get_quick_filter_query()
    except NotImplementedError:
        assert True
    else:
        assert False


def test_form_rendering_with_request_get_args():
    request = HttpRequest()
    request.GET['search'] = 'cats'
    request.GET['my_filters'] = 'published'

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
        assert inp.get('name') == 'my_filters'

    # check if we marked selected filter
    assert filters_inputs[0].attrs.get('checked') == ''
