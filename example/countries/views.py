from __future__ import (absolute_import, unicode_literals)

import requests

from django.utils.translation import ugettext as _

from arctic.generics import DataListView
from arctic.utils import RemoteDataSet


class CountryListView(DataListView):
    paginate_by = 2
    dataset = CountriesDataSet(paginate_by)
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
    permission_required = 'country_view'


class CountriesDataSet(RemoteDataSet):
    url_template = 'https://restcountries.eu/rest/v2{filters}'
    filters_template_kv = '/{key}/{value}'
    paginate_by = 10

    def get(self, page):
        r = requests.get(self.get_url())
        print r.json
        return r.json()
