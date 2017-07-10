from __future__ import (absolute_import, unicode_literals)

import json
from six.moves import urllib

from django.utils.safestring import mark_safe

from arctic.generics import DataListView
from arctic.utils import RemoteDataSet


class CompaniesDataSet(RemoteDataSet):
    base_url = 'https://overheid.io/api/kvk?ovio-api-key='
    api_key = 'dac8ed4b7744a44a3a88fb2395eb5edacb1fb173837b928deb74fdf89bcec00a'
    url_template = '{}{}'.format(base_url, api_key)
    # filters_template_kv = '/{key}/{value}'

    _count = None

    @property
    def count(self):
        # self._count gets overwritten on every request
        if self._count is None:
            return self.get(1, 1)
        return self._count

    def get(self, page, paginate_by):
        url = self.get_url(page, paginate_by)
        r = urllib.request.urlopen((url))
        data = r.read().decode("utf-8")
        data = json.loads(data)
        self._count = data['totalItemCount']
        return data['_embedded']['rechtspersoon']

    def get_url(self, page, page_size):
        url = self.url_template + '&page={}&size={}'.format(page, page_size)
        return url.replace('?&', '?')


class CompanyListView(DataListView):
    paginate_by = 20
    dataset = CompaniesDataSet()
    fields = ['handelsnaam', 'dossiernummer']
    # ordering_fields = ['name', 'topLevelDomain']
    # search_fields = ['name']
    # breadcrumbs = (('Home', 'index'), ('Country List', None))
    # filter_fields = ['published']
    permission_required = 'company_view'
