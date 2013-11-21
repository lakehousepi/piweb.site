from django.views.generic import TemplateView
from piweb.models import TempReading, TempSeries
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class TestView(TemplateView):
    template_name = 'piweb/test.html'
    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context['svgtext'] = 'Hello New World'
        return context