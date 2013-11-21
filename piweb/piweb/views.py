from django.views.generic import TemplateView
from piweb.models import TempReading, TempSeries
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import StringIO

class TestView(TemplateView):
    template_name = 'piweb/test.html'
    def get_context_data(self, **kwargs):
        data = np.random.randn(10) * 20
        x = data + np.random.randn(10)
        y = 3 * data + np.random.randn(10)
        
        fig = Figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(x, y, c='b')
        fig.set(facecolor='g')
        canvas = FigureCanvas(fig)
        
        imgdata = StringIO.StringIO()
        canvas.print_svg(imgdata, transparent=True)
        
        imgstr = imgdata.getvalue()
        
        context = super(TestView, self).get_context_data(**kwargs)
        context['svgtext'] = imgstr
        
        return context