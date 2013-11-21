from django.views.generic import TemplateView

class TestView(TemplateView):
    template_name = 'piweb/test.html'
    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context['svgtext'] = 'Hello New World'
        return context