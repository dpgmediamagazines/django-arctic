import pytest
from collections import OrderedDict

from arctic.mixins import FormMixin
from articles.forms import ArticleForm

from tests.conftest import get_form
from tests.factories import ArticleFactory


@pytest.fixture
def layout():
    class Layout(FormMixin):
        layout = None

        def __init__(self):
            self.object = ArticleFactory()
            self.form = ArticleForm(instance=self.object)
            self.get_form = get_form(self.form)

    return Layout()


pytestmark = pytest.mark.django_db


def test_layout_example_1(layout):
    layout.layout = ['title|8']
    layout = layout.get_layout()

    assert layout[0]['fieldset']['title'] is None
    assert layout[0]['fieldset']['description'] is None
    assert layout[0]['fieldset']['collapsible'] is None
    assert layout[0]['rows'][0]['name'] == 'title'
    assert layout[0]['rows'][0]['column'] == '8'


def test_layout_example_2(layout):
    layout.layout = [['title|3', 'title', 'title']]
    layout = layout.get_layout()

    assert layout[0]['fieldset']['title'] is None
    assert layout[0]['fieldset']['description'] is None
    assert layout[0]['fieldset']['collapsible'] is None
    assert layout[0]['rows'][0][0]['name'] == 'title'
    assert layout[0]['rows'][0][0]['column'] == '3'
    assert layout[0]['rows'][0][1]['name'] == 'title'
    assert layout[0]['rows'][0][1]['column'] == '4'
    assert layout[0]['rows'][0][2]['name'] == 'title'
    assert layout[0]['rows'][0][2]['column'] == '5'


def test_layout_example_3a(layout):
    layout.layout = [['title|3', 'title', 'title', 'category', 'category']]
    layout = layout.get_layout()

    assert layout[0]['fieldset']['title'] is None
    assert layout[0]['fieldset']['description'] is None
    assert layout[0]['fieldset']['collapsible'] is None
    assert layout[0]['rows'][0][0]['name'] == 'title'
    assert layout[0]['rows'][0][0]['column'] == '3'
    assert layout[0]['rows'][0][1]['name'] == 'title'
    assert layout[0]['rows'][0][1]['column'] == '2'
    assert layout[0]['rows'][0][2]['name'] == 'title'
    assert layout[0]['rows'][0][2]['column'] == '2'
    assert layout[0]['rows'][0][3]['name'] == 'category'
    assert layout[0]['rows'][0][3]['column'] == '2'
    assert layout[0]['rows'][0][4]['name'] == 'category'
    assert layout[0]['rows'][0][4]['column'] == '3'


def test_layout_example_3b(layout):
    layout.layout = ['title|3', 'title', 'title', ['category', 'category']]
    layout = layout.get_layout()

    assert layout[0]['fieldset']['title'] is None
    assert layout[0]['fieldset']['description'] is None
    assert layout[0]['fieldset']['collapsible'] is None
    assert layout[0]['rows'][0]['name'] == 'title'
    assert layout[0]['rows'][0]['column'] == '3'
    assert layout[0]['rows'][1]['name'] == 'title'
    assert layout[0]['rows'][1]['column'] is None
    assert layout[0]['rows'][2]['name'] == 'title'
    assert layout[0]['rows'][2]['column'] is None
    assert layout[0]['rows'][3][0]['name'] == 'category'
    assert layout[0]['rows'][3][0]['column'] == '6'
    assert layout[0]['rows'][3][1]['name'] == 'category'
    assert layout[0]['rows'][3][1]['column'] == '6'


def test_layout_example_4(layout):
    layout.layout = OrderedDict([('-fieldset',
                                  ['title',
                                   'title',
                                   ['category', 'updated_at|4']]),
                                ('fieldset2|test description',
                                 [['title|7', 'category']]),
                                ('+fieldset3',
                                 ['published'])])
    layout = layout.get_layout()

    assert layout[0]['fieldset']['title'] == 'fieldset'
    assert layout[0]['fieldset']['description'] is None
    assert layout[0]['fieldset']['collapsible'] == 'closed'
    assert layout[0]['rows'][0]['name'] == 'title'
    assert layout[0]['rows'][0]['column'] is None
    assert layout[0]['rows'][1]['name'] == 'title'
    assert layout[0]['rows'][1]['column'] is None
    assert layout[0]['rows'][2][0]['name'] == 'category'
    assert layout[0]['rows'][2][0]['column'] == '8'
    assert layout[0]['rows'][2][1]['name'] == 'updated_at'
    assert layout[0]['rows'][2][1]['column'] == '4'

    assert layout[1]['fieldset']['title'] == 'fieldset2'
    assert layout[1]['fieldset']['description'] == 'test description'
    assert layout[1]['fieldset']['collapsible'] is None
    assert layout[1]['rows'][0][0]['name'] == 'title'
    assert layout[1]['rows'][0][0]['column'] == '7'
    assert layout[1]['rows'][0][1]['name'] == 'category'
    assert layout[1]['rows'][0][1]['column'] == '5'

    assert layout[2]['fieldset']['title'] == 'fieldset3'
    assert layout[2]['fieldset']['description'] is None
    assert layout[2]['fieldset']['collapsible'] == 'open'
    assert layout[2]['rows'][0]['name'] == 'published'
    assert layout[2]['rows'][0]['column'] is None
