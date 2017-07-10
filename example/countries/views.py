from __future__ import (absolute_import, unicode_literals)

import json
from six.moves import urllib

from django.utils.safestring import mark_safe

from arctic.generics import DataListView
from arctic.utils import RemoteDataSet


class CountriesDataSet(RemoteDataSet):
    url_template = 'https://restcountries.eu/rest/v2{filters}'
    filters_template_kv = '/{key}/{value}'

    def get(self, page, paginate_by):
        r = urllib.request.urlopen((self.get_url(page, paginate_by)))
        offset = (page - 1) * paginate_by
        limit = offset + paginate_by
        data = r.read().decode("utf-8")
        return json.loads(data)[offset:limit]

    def __len__(self):
        return len(self.get(1, -1))


class CountryListView(DataListView):
    paginate_by = 5
    dataset = CountriesDataSet()
    fields = ['name', 'topLevelDomain', 'capital', 'flag']
    ordering_fields = ['name', 'topLevelDomain']
    search_fields = ['name']
    breadcrumbs = (('Home', 'index'), ('Country List', None))
    filter_fields = ['published']
    permission_required = 'country_view'

    def get_flag_field(self, obj):
        return mark_safe('<div style="width: 3em;"><img src="{}" /></div>'.
                         format(obj['flag']))
