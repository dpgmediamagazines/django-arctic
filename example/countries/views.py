from __future__ import (absolute_import, unicode_literals)

from django.utils.translation import ugettext as _

from arctic.generics import DataListView
from collections import OrderedDict


class CountryListView(DataListView):
    url_template = 'https://restcountries.eu/rest/v2/{options}'
    paginate_by = 2
    fields = ['name', 'topLevelDomain', 'capital', 'translations', 'flag']
    ordering_fields = ['name', 'topLevelDomain']
    search_fields = ['name']
    breadcrumbs = (('Home', 'index'), ('Country List', None))
    field_links = {
        'title': 'articles:detail',
        'published': 'articles:detail',
        'category': ('articles:category-detail', 'category_id'),
    }

    filter_fields = ['published']
    permission_required = "articles_view"


class RemoteDataSet():
    url_template = None
    options = []
    offset = 0
    limit = None
    order = ''
    fields = []
    filters = ''

    def init(self, url_template, fields=None):
        self.url_template = url_template
        self.fields = fields

    def filter(self, **kwargs):
        self.filters = ''
        template = '/{key}/{value}'
        for key, value in kwargs.items():
            self.filters += template.format(key=key, value=value)

        return self

    def order_by(self, ):
        pass

    def get():
        options = filters + '?' + order + '&fields=' + fields.join(',')
