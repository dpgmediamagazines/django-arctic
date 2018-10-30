from arctic.generics import TemplateView


class DashboardView(TemplateView):
    page_title = "Dashboard"
    template_name = "dashboard.html"
    permission_required = "view_dashboard"
