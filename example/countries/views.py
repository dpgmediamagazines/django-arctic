from __future__ import absolute_import, unicode_literals

import json
import os
from six.moves import urllib

from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView

from arctic.generics import DataListView
from arctic.utils import RemoteDataSet, offset_limit


class CountryAPIView(TemplateView):
    """
    Mock API used to demonstrate the usage of DataListView
    It's a simple implementation with support for sorting, pagination,
    filtering and field selection.
    """

    def render_to_response(self, context, **response_kwargs):
        data = []
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "countries.json"), "r") as f:
            data = json.loads(f.read())

        if data:
            all_fields = data[0].keys()

        for field in all_fields:
            value = self.request.GET.get(field, None)
            if value:
                data = list(
                    filter(lambda d: value.lower() in d[field].lower(), data)
                )

        if self.request.GET.get("fields"):
            fields = self.request.GET.get("fields").split(",")
            fields = set(all_fields).intersection(fields)
            temp = []
            for row in data:
                temp_row = {}
                for field in fields:
                    temp_row[field] = row[field]
                temp.append(temp_row)
            data = temp

        if self.request.GET.get("order_by"):
            order_by = self.request.GET.get("order_by")
            reverse = False
            if order_by[0] == "-":
                reverse = True
                order_by = order_by[1:]

            data = sorted(data, key=lambda k: k[order_by], reverse=reverse)

        if self.request.GET.get("offset") or self.request.GET.get("limit"):
            offset = int(self.request.GET.get("offset", 0))
            limit = min(
                int(self.request.GET.get("limit", len(data) - offset)),
                len(data) - offset,
            )
            if offset > len(data) or (offset + limit) > len(data):
                data = []
            else:
                data = data[offset : limit + offset]

        return JsonResponse(data, safe=False, **response_kwargs)


class CountriesDataSet(RemoteDataSet):
    url_template = "countries-api/?{filters}{fields}{order}{paginate}"
    order_template = "&order_by={}"

    @offset_limit
    def get(self, offset, limit):
        r = urllib.request.urlopen((self.get_url(offset, limit)))
        data = r.read().decode("utf-8")
        return json.loads(data)


class CountryListView(DataListView):
    paginate_by = 10
    dataset = CountriesDataSet()
    fields = ["name", "capital", "flag"]
    ordering_fields = ["name", "capital"]
    search_fields = ["name"]
    breadcrumbs = (("Home", "index"), ("Country List", None))
    page_title = "Countries"
    permission_required = "country_view"

    def get_context_data(self, **kwargs):
        # small hack to setup the current host in the url of the local API
        if not self.dataset.url_template.startswith("http"):
            self.dataset.url_template = "{}://{}/{}".format(
                self.request.scheme,
                self.request.get_host(),
                self.dataset.url_template,
            )
        context = super(CountryListView, self).get_context_data(**kwargs)
        return context

    def get_flag_field(self, obj):
        return mark_safe(
            '<img style="max-width: 2rem" src="{}" />'.format(obj["flag"])
        )
