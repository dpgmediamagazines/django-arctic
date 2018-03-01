from django.db.models import Q
from django.http import HttpRequest
from django.template import Context, Template
from bs4 import BeautifulSoup

from arctic.forms import (
    QuickFiltersForm,
    SimpleSearchForm
)


class FiltersForm(QuickFiltersForm):
    FILTER_BUTTONS = (
        ('current', 'Currently visible'),
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    )


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


def test_quick_filters_form():
    form = FiltersForm()

    assert hasattr(form, 'get_current_filter')
    assert form.filters_field_name == 'quick_filters'


def test_quick_filters_form_error():
    class EmptyFiltersForm(QuickFiltersForm):
        pass

    try:
        EmptyFiltersForm()
    except AttributeError as error:
        assert error


def test_context_in_quick_filters_widget():
    form = FiltersForm(request='request_obj')

    widget = form.fields[form.filters_field_name].widget
    context = widget.get_context('quick_filters', 'past', widget.attrs)

    assert context.get('request') == 'request_obj'
    assert widget.template_name == 'arctic/widgets/quick_filters_select.html'


def test_form_rendering_with_request_get_args():
    request = HttpRequest()
    request.GET['search'] = 'cats'
    request.GET['quick_filters'] = 'current'

    form = FiltersForm(request=request, data=request.GET)
    assert form.is_valid()

    template = Template('{{ form }}').render(Context({"form": form}))

    soup = BeautifulSoup(template, 'html.parser')

    filters_links = soup.find_all('a')

    assert len(filters_links) == len(form.FILTER_BUTTONS)

    for a, btn in zip(filters_links, form.FILTER_BUTTONS):
        assert a.text.strip() == btn[1]
        # check active filter button
        if btn[0] == form.FILTER_BUTTONS[0][0]:  # 'current'
            assert 'btn-info' in a['class']
            assert a['href'] == '?search=cats&'
        else:
            assert a['href'] == '?search=cats&quick_filters={}'.format(btn[0])
