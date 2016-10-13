# from __future__ import absolute_import, unicode_literals
#
# import django
# from django import forms
# from django.test import TestCase
#
# from ..mixins import LayoutMixin
#
# from collections import OrderedDict
#
#
# class TestForm(forms.Form):
#     title = forms.CharField(max_length=100)
#     description = forms.CharField(max_length=100)
#     updated_at = forms.CharField(max_length=100, required=False)
#     category = forms.CharField(max_length=100, required=False)
#     published = forms.CharField(max_length=100, required=False)
#
#
# class LayoutMixinTestCase(LayoutMixin, TestCase):
#     """Tests for the ``InvoiceDetailView`` generic class based view."""
#     def setUp(self):
#         self.form = TestForm()
#         self.form.title = 'title'
#         self.form.description = 'description'
#         self.form.category = 'category'
#         self.form.updated_at = 'updated_at'
#         self.form.published = 'published'
#
#     def get_form(self):
#         return self.form
#
#     def test_layout_1(self):
#         self.layout = ['title|8']
#         layout = self.get_layout()
#
#         assert layout[0][0]['name'] == 'title'
#         assert layout[0][0]['column'] == '8'
#
#     def test_layout_2(self):
#         self.layout = ['title|3', 'title', 'title']
#         layout = self.get_layout()
#
#         assert layout[0][0]['name'] == 'title'
#         assert layout[0][0]['column'] == '3'
#         assert layout[0][1]['name'] == 'title'
#         assert layout[0][1]['column'] == '4'
#         assert layout[0][2]['name'] == 'title'
#         assert layout[0][2]['column'] == '5'
#
#     def test_layout_3a(self):
#         self.layout = ['title|3', 'title', 'title', 'category', 'category']
#         layout = self.get_layout()
#
#         assert layout[0][0]['name'] == 'title'
#         assert layout[0][0]['column'] == '3'
#         assert layout[0][1]['name'] == 'title'
#         assert layout[0][1]['column'] == '2'
#         assert layout[0][2]['name'] == 'title'
#         assert layout[0][2]['column'] == '2'
#         assert layout[0][3]['name'] == 'category'
#         assert layout[0][3]['column'] == '2'
#         assert layout[0][4]['name'] == 'category'
#         assert layout[0][4]['column'] == '3'
#
#     def test_layout_3b(self):
#         self.layout = ['title|3', 'title', 'title', ['category', 'category']]
#         layout = self.get_layout()
#
#         assert layout[0][0]['name'] == 'title'
#         assert layout[0][0]['column'] == '3'
#         assert layout[0][1]['name'] == 'title'
#         assert layout[0][1]['column'] == '4'
#         assert layout[0][2]['name'] == 'title'
#         assert layout[0][2]['column'] == '5'
#         assert layout[0][3][0]['name'] == 'category'
#         assert layout[0][3][0]['column'] == '6'
#         assert layout[0][3][1]['name'] == 'category'
#         assert layout[0][3][1]['column'] == '6'
#
#     def test_layout_4(self):
#         self.layout = OrderedDict([('-fieldset', [
#                                        'title',
#                                        'title',
#                                        ['category', 'updated_at|4']
#                                    ]),
#                                    ('fieldset2', [
#                                        ['title|7', 'category'],
#                                    ]),
#                                    ('fieldset3', [
#                                        'published'
#                                    ])])
#
#         layout = self.get_layout()
#
#         assert layout['-fieldset'][0]['name'] == 'title'
#         assert layout['-fieldset'][0]['column'] is None
#         assert layout['-fieldset'][1]['name'] == 'title'
#         assert layout['-fieldset'][1]['column'] is None
#         assert layout['-fieldset'][2][0]['name'] == 'category'
#         assert layout['-fieldset'][2][0]['column'] == '8'
#         assert layout['-fieldset'][2][1]['name'] == 'updated_at'
#         assert layout['-fieldset'][2][1]['column'] == '4'
#         assert layout['fieldset2'][0][0]['name'] == 'title'
#         assert layout['fieldset2'][0][0]['column'] == '7'
#         assert layout['fieldset2'][0][1]['name'] == 'category'
#         assert layout['fieldset2'][0][1]['column'] == '5'
#         assert layout['fieldset3'][0]['name'] == 'published'
#         assert layout['fieldset3'][0]['column'] is None
