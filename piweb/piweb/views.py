import datetime as dt
from dateutil.relativedelta import relativedelta
import pytz

from django.views.generic import TemplateView
from django.shortcuts import render
from piweb.models import TempReading, TempSeries

import numpy as np
import pandas as pd

import StringIO
import base64
import psutil
from debug_toolbar_line_profiler import profile_additional

from utils import graphing as pwgraph

class HomeView(TemplateView):
    template_name = 'piweb/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        latest = TempReading.objects.filter(tempseries__name='Upstairs').order_by('-timestamp')[0]
        context['latest'] = latest
        return context

class FourChartsDynamicView(TemplateView):
    template_name = 'piweb/fourchartsdynamic.html'

    def get_context_data(self, **kwargs):
        context = super(FourChartsView, self).get_context_data(**kwargs)
        fig = pwgraph.make_four_graphs()

        pngdata = StringIO.StringIO()
        fig.savefig(pngdata, format='png', facecolor='w', bbox_inches='tight')


        context['pngstr'] = base64.b64encode(pngdata.getvalue())
        return context

class FourChartsStaticView(TemplateView):
    template_name = 'piweb/fourchartsstatic.html'

class TableView(TemplateView):
    template_name = 'piweb/table.html'

    def get_context_data(self, **kwargs):
        context = super(TableView, self).get_context_data(**kwargs)

        tz = pytz.timezone('America/New_York')
        now = dt.datetime.now(pytz.timezone('America/New_York'))
        daysback = kwargs.get('daysback', 1)
        starttime = now - relativedelta(days=daysback)
        upstairs = TempSeries.objects.get(name='Upstairs')
        upstairstemps = upstairs\
                            .tempreading_set.filter(timestamp__gte=starttime)\
                            .order_by('timestamp')

        df = pd.DataFrame(list(upstairstemps.values()))
        df = df.set_index('timestamp')

        context['df'] = df
        context['tablehtml'] = df.to_html()
        context['idxtype'] = type(list(df.index)[0]))
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
