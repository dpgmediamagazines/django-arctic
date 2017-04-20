from __future__ import (absolute_import, unicode_literals)

import requests

from django.utils.translation import ugettext as _

from arctic.generics import DataListView
from arctic.utils import RemoteDataSet


class CountriesDataSet(RemoteDataSet):
    url_template = 'https://restcountries.eu/rest/v2{filters}'
    filters_template_kv = '/{key}/{value}'

    def get(self, page, paginate_by):
        r = requests.get(self.get_url(page, paginate_by))
        offset = (page - 1) * paginate_by
        limit = offset + paginate_by
        return r.json()[offset:limit]


class CountryListView(DataListView):
    paginate_by = 2
    dataset = CountriesDataSet()
    fields = ['name', 'topLevelDomain', 'capital', 'flag']
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
