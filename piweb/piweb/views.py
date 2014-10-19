from django.views.generic import TemplateView
from django.shortcuts import render
from piweb.models import TempReading, TempSeries
import numpy as np
import pandas as pd
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sbn
import StringIO
from debug_toolbar_line_profiler import profile_additional

class TestView(TemplateView):
    template_name = 'piweb/test.html'
    
    def get_context_data(self, **kwargs):
        upstairs = TempSeries.objects.get(name='Upstairs')
        upstairstemps = upstairs.tempreading_set.all().order_by('-timestamp')[:22464]

        frame = pd.DataFrame(list(upstairstemps.values()))
        frame.set_index('timestamp', inplace=True)
        
        # matplotlib.rcParams['svg.fonttype'] = 'none'

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
        context['htmltable'] = frame[:12].to_html()

        return context

def testview2(request):
    df = pd.DataFrame({'a': np.random.randn(10), 'b': np.random.randn(10)})
    htmltable = df.to_html()
    context = {}
    context['htmltable'] = htmltable

    return render(request, 'piweb/test2.html', context)

@profile_additional(TestView.get_context_data)
def testview3(request):
    return TestView.as_view()(request)
