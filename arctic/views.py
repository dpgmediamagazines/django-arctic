from django.utils.translation import ugettext as _

from arctic.generics import TemplateView


class BadRequestView(TemplateView):
    page_title = 'Bad Request'
    template_name = 'arctic/400.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=400)


class ForbiddenView(TemplateView):
    page_title = 'Access Forbidden'
    template_name = 'arctic/403.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)


class NotFoundView(TemplateView):
    page_title = 'Page not Found'
    template_name = 'arctic/404.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)


class InternalErrorView(TemplateView):
    page_title = 'Internal Error'
    template_name = 'arctic/500.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=500)

handler400 = BadRequestView.as_view()
handler403 = ForbiddenView.as_view()
handler404 = NotFoundView.as_view()
handler500 = InternalErrorView.as_view()

