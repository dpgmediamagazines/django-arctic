import importlib

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic.base import View as BaseView

from arctic.generics import TemplateView


class BadRequestView(TemplateView):
    page_title = 'Bad Request'
    template_name = 'arctic/400.html'
    permission_required = ''

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=400)


class ForbiddenView(TemplateView):
    page_title = 'Access Forbidden'
    template_name = 'arctic/403.html'
    permission_required = ''

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)


class NotFoundView(TemplateView):
    page_title = 'Page not Found'
    template_name = 'arctic/404.html'
    permission_required = ''

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)


class InternalErrorView(TemplateView):
    page_title = 'Internal Error'
    template_name = 'arctic/500.html'
    permission_required = ''

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=500)


class AutoCompleteView(BaseView):
    max_items = 10

    def get_data(self, model, field, search):
        field_startswith = {field + '__istartswith': search}
        max_items = self.max_items
        data = []
        if search:
            for row in model.objects.filter(**field_startswith)[:max_items]:
                data.append({'label': getattr(row, field), 'value': row.pk})
        return {'options': data}

    def get(self, request, *args, **kwargs):
        if settings.DEBUG or request.is_ajax():
            model_name, field = settings.ARCTIC_AUTOCOMPLETE[
                kwargs['resource']]
            model_path = '.'.join(model_name.split('.')[:-1]) + '.models'
            model_package = importlib.import_module(model_path)
            model = getattr(model_package, model_name.split('.')[-1])
            context = self.get_data(model, field, kwargs['search'])
            return self.render_to_response(context)
        raise PermissionDenied

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)


handler400 = BadRequestView.as_view()
handler403 = ForbiddenView.as_view()
handler404 = NotFoundView.as_view()
handler500 = InternalErrorView.as_view()
