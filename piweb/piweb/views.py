from django.views.generic import TemplateView
from django.shortcuts import render
from piweb.models import TempReading, TempSeries

import numpy as np
import pandas as pd

import matplotlib as mpl
mpl.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sbn

import StringIO
import base64
import psutil
import datetime as dt
import pytz
from dateutil.relativedelta import relativedelta
from debug_toolbar_line_profiler import profile_additional

class HomeView(TemplateView):
    template_name = 'piweb/home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

class FourChartsView(TemplateView):
    template_name = 'piweb/fourcharts.html'

    def get_context_data(self, **kwargs):
        now = dt.datetime.now(pytz.timezone('America/New_York'))
        ayearago = now - relativedelta(years=1)
        
        upstairs = TempSeries.objects.get(name='Upstairs')
        upstairstemps = upstairs\
                            .tempreading_set.filter(timestamp__gte=ayearago)\
                            .order_by('timestamp')
        
        df = pd.DataFrame(list(upstairstemps.values()))
        df = df.set_index('timestamp')
                
        fig, axes = plt.subplots(2, 2, figsize=(15, 8), dpi=200)
        for (i, d), rsamp in zip(enumerate([360, 30, 7, 1]), ['d', 'h', None, None]):
            ax = axes.flatten()[i]
            earlycut = now - relativedelta(days=d)
            data = df.loc[df.index>=earlycut, :]
            if rsamp:
                data = data.resample(rule=rsamp, how='mean')
            ax.plot(data.index, data['value'])
            
            ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
            ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())

            ax.grid(b=True, which='major', color='w', linewidth=1.5)
            ax.grid(b=True, which='minor', color='w', linewidth=0.75)
                              
            plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
            
            ax.set_title('Temperature data going back %d days' % d)

        fig.tight_layout()

        pngdata = StringIO.StringIO()
        fig.savefig(pngdata, format='png', facecolor='w', bbox_inches='tight')
        
        context = super(FourChartsView, self).get_context_data(**kwargs)
        # context['svgstr'] = svgstr
        context['pngstr'] = base64.b64encode(pngdata.getvalue())
        # assert(0==1)

        return context

class TestView(TemplateView):
    template_name = 'piweb/test.html'
    
    def get_context_data(self, **kwargs):
        lim = self.request.GET.get('limit', 3000)

        upstairs = TempSeries.objects.get(name='Upstairs')
        upstairstemps = upstairs.tempreading_set.all().order_by('-timestamp')[:lim]

        frame = pd.DataFrame(list(upstairstemps.values()))
        frame.set_index('timestamp', inplace=True)
        
        # matplotlib.rcParams['svg.fonttype'] = 'none'

        fig, ax = plt.subplots(1,1, figsize=(10, 10))
        frame['value'].plot(ax=ax)
        ax.get_xaxis().grid(color='w', linewidth=1)
    	ax.get_yaxis().grid(color='w', linewidth=1)

        fig.set(facecolor='w')
        fig.tight_layout()

        svgdata = StringIO.StringIO()
        fig.savefig(svgdata, format='svg', facecolor='w', bbox_inches='tight')
        
        context = super(TestView, self).get_context_data(**kwargs)
        # context['svgstr'] = svgstr
        context['svgtext'] = svgdata.getvalue()
        context['htmltable'] = frame[:12].to_html()
        context['mempct'] = psutil.virtual_memory().percent

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
