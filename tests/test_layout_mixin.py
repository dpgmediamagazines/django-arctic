from collections import OrderedDict
from django.test import TestCase

from arctic.mixins import LayoutMixin
from .conftest import article, article_form, get_form


class LayoutMixinTestCase(LayoutMixin, TestCase):

    def setUp(self):
        self.object = article()
        self.form = article_form()
        self.get_form = get_form(self.form)

    def test_layout_example_0(self):
        self.layout = ['title|8']
        layout = self.get_layout()

        assert layout[(0, None, False)][0]['name'] == 'title'
        assert layout[(0, None, False)][0]['column'] == '8'

    def test_layout_example_1(self):
        self.layout = ['title|8']
        layout = self.get_layout()

        assert layout[(0, None, False)][0]['name'] == 'title'
        assert layout[(0, None, False)][0]['column'] == '8'

    def test_layout_example_2(self):
        self.layout = [['title|3', 'title', 'title']]
        layout = self.get_layout()
        print(layout)

        assert layout[(0, None, False)][0][0]['name'] == 'title'
        assert layout[(0, None, False)][0][0]['column'] == '3'
        assert layout[(0, None, False)][0][1]['name'] == 'title'
        assert layout[(0, None, False)][0][1]['column'] == '4'
        assert layout[(0, None, False)][0][2]['name'] == 'title'
        assert layout[(0, None, False)][0][2]['column'] == '5'

    def test_layout_example_3a(self):
        self.layout = [['title|3', 'title', 'title', 'category', 'category']]
        layout = self.get_layout()

        assert layout[(0, None, False)][0][0]['name'] == 'title'
        assert layout[(0, None, False)][0][0]['column'] == '3'
        assert layout[(0, None, False)][0][1]['name'] == 'title'
        assert layout[(0, None, False)][0][1]['column'] == '2'
        assert layout[(0, None, False)][0][2]['name'] == 'title'
        assert layout[(0, None, False)][0][2]['column'] == '2'
        assert layout[(0, None, False)][0][3]['name'] == 'category'
        assert layout[(0, None, False)][0][3]['column'] == '2'
        assert layout[(0, None, False)][0][4]['name'] == 'category'
        assert layout[(0, None, False)][0][4]['column'] == '3'

    def test_layout_example_3b(self):
        self.layout = ['title|3', 'title', 'title', ['category', 'category']]
        layout = self.get_layout()

        assert layout[(0, None, False)][0]['name'] == 'title'
        assert layout[(0, None, False)][0]['column'] == '3'
        assert layout[(0, None, False)][1]['name'] == 'title'
        assert layout[(0, None, False)][1]['column'] is None
        assert layout[(0, None, False)][2]['name'] == 'title'
        assert layout[(0, None, False)][2]['column'] is None
        assert layout[(0, None, False)][3][0]['name'] == 'category'
        assert layout[(0, None, False)][3][0]['column'] == '6'
        assert layout[(0, None, False)][3][1]['name'] == 'category'
        assert layout[(0, None, False)][3][1]['column'] == '6'

    def test_layout_example_4(self):
        self.layout = OrderedDict([('-fieldset', [
                                       'title',
                                       'title',
                                       ['category', 'updated_at|4']
                                   ]),
                                   ('fieldset2', [
                                       ['title|7', 'category'],
                                   ]),
                                   ('fieldset3', [
                                       'published'
                                   ])])

        layout = self.get_layout()
        print(layout)

        assert layout[('fieldset', None, True)][0]['name'] == 'title'
        assert layout[('fieldset', None, True)][0]['column'] is None
        assert layout[('fieldset', None, True)][1]['name'] == 'title'
        assert layout[('fieldset', None, True)][1]['column'] is None
        assert layout[('fieldset', None, True)][2][0]['name'] == 'category'
        assert layout[('fieldset', None, True)][2][0]['column'] == '8'
        assert layout[('fieldset', None, True)][2][1]['name'] == 'updated_at'
        assert layout[('fieldset', None, True)][2][1]['column'] == '4'
        assert layout[('fieldset2', None, False)][0][0]['name'] == 'title'
        assert layout[('fieldset2', None, False)][0][0]['column'] == '7'
        assert layout[('fieldset2', None, False)][0][1]['name'] == 'category'
        assert layout[('fieldset2', None, False)][0][1]['column'] == '5'
        assert layout[('fieldset3', None, False)][0]['name'] == 'published'
        assert layout[('fieldset3', None, False)][0]['column'] is None
