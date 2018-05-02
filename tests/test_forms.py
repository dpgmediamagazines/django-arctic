from django.db.models import Q
# from django.http import HttpRequest
# from django.template import Context, Template
# from bs4 import BeautifulSoup

from arctic.forms import SimpleSearchForm
from arctic.widgets import QuickFiltersSelect


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


# def test_form_rendering_with_request_get_args():
#     request = HttpRequest()
#     request.GET['search'] = 'cats'
#     request.GET['my_filters'] = 'published'

#     form = FiltersForm(data=request.GET)
#     assert form.is_valid()

#     template = Template('{{ form }}').render(Context({"form": form}))

#     soup = BeautifulSoup(template, 'html.parser')

#     filters_inputs = soup.find_all('input', {'type': 'checkbox'})
#     filters_buttons = soup.find_all('label', {'class': 'btn'})

#     assert len(filters_inputs) == len(form.FILTER_BUTTONS)
#     assert len(filters_buttons) == len(form.FILTER_BUTTONS)

#     for inp, btn, choice in zip(
#             filters_inputs,
#             filters_buttons,
#             form.FILTER_BUTTONS):
#         assert btn.text.strip() == choice[1]
#         assert inp.get('value') == choice[0]
#         assert inp.get('name') == 'my_filters'

#     # check if we marked selected filter
#     assert filters_inputs[0].attrs.get('checked') == ''


# def test_filters_form_rendering_select_one():
#     request = HttpRequest()
#     request.GET['search'] = 'cats'
#     request.GET['my_filters'] = 'published'

#     form = FiltersFormSelectOne(data=request.GET)
#     assert form.is_valid()

#     template = Template('{{ form }}').render(Context({"form": form}))

#     soup = BeautifulSoup(template, 'html.parser')
#     filters_inputs = soup.find_all('input', {'type': 'checkbox'})

#     assert filters_inputs[0].attrs.get('checked') is None
