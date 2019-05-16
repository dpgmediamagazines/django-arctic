import importlib
import json

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView as BaseTemplateView
from django.views.generic.base import View as BaseView

from arctic.generics import TemplateView


class BadRequestView(TemplateView):
    page_title = "Bad Request"
    template_name = "arctic/400.html"
    permission_required = ""

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=400)


class ForbiddenView(TemplateView):
    page_title = "Access Forbidden"
    template_name = "arctic/403.html"
    permission_required = ""

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)


class NotFoundView(TemplateView):
    page_title = "Page not Found"
    template_name = "arctic/404.html"
    permission_required = ""

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)


def handler500(request, template_name="arctic/500.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response


class AutoCompleteView(BaseView):
    max_items = 10

    def get_data(self, model, field, search):
        field_startswith = {field + "__istartswith": search}
        max_items = self.max_items
        data = []
        if search:
            for row in model.objects.filter(**field_startswith)[:max_items]:
                data.append({"label": getattr(row, field), "value": row.pk})
        return {"options": data}

    def get(self, request, *args, **kwargs):
        if settings.DEBUG or request.is_ajax():
            model_name, field = settings.ARCTIC_AUTOCOMPLETE[
                kwargs["resource"]
            ]
            model_path = ".".join(model_name.split(".")[:-1]) + ".models"
            model_package = importlib.import_module(model_path)
            model = getattr(model_package, model_name.split(".")[-1])
            context = self.get_data(model, field, kwargs["search"])
            return self.render_to_response(context)
        raise PermissionDenied

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)


class OrderView(BaseView):
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderView, self).dispatch(request, *args, **kwargs)

    def post(self, request, resource):
        if settings.DEBUG or request.is_ajax():
            m, v = resource.rsplit(".", 1)
            module = importlib.import_module(m)
            view = getattr(module, v)
            view.reorder(json.loads(request.body))
            return HttpResponse(status=201)
        raise PermissionDenied


class RedirectToParentView(BaseTemplateView):
    template_name = "arctic/redirect_to_parent.html"


handler400 = BadRequestView.as_view()
handler403 = ForbiddenView.as_view()
handler404 = NotFoundView.as_view()
