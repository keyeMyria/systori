from django.views.generic import TemplateView
from ..task.models import LineItem

class SettingsView(TemplateView):
    template_name = "main/settings.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context

class DashboardView(TemplateView):
    template_name = "main/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['flagged_lineitems'] = LineItem.objects.filter(is_flagged=True)
        return context

class IndexView(TemplateView):
    template_name = "main/front_page.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            view = DashboardView.as_view()
            return view(request, *args, **kwargs)
        return super(IndexView, self).dispatch(request, *args, **kwargs)
