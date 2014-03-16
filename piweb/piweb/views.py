from django.views.generic import TemplateView
from piweb.models import TempReading, TempSeries
import numpy as np
import pandas as pd
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sbn
import StringIO

class TestView(TemplateView):
    template_name = 'piweb/test.html'
    def get_context_data(self, **kwargs):
        upstairs = TempSeries.objects.get(name='Upstairs')
        upstairstemps = upstairs.tempreading_set.all().order_by('-timestamp')[:300]

        frame = pd.DataFrame(list(upstairstemps.values()))
        frame.set_index('timestamp', inplace=True)
       
        matplotlib.rcParams['svg.fonttype'] = 'none'

        fig = Figure()
        ax = fig.add_subplot(1,1,1)
        frame['value'].plot(ax=ax)
        ax.get_xaxis().grid(color='w', linewidth=1)
    	ax.get_yaxis().grid(color='w', linewidth=1)

        fig.set(facecolor='w')
        canvas = FigureCanvas(fig)
        
        imgdata = StringIO.StringIO()
        canvas.print_svg(imgdata)
        
        imgstr = imgdata.getvalue()
        
        context = super(TestView, self).get_context_data(**kwargs)
        context['svgtext'] = imgstr
        
        return context
