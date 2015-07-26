import os

import datetime as dt
import pytz
from dateutil.relativedelta import relativedelta

import numpy as np
import pandas as pd

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sbn

from piweb.models import TempReading, TempSeries
from django.conf import settings

def make_four_graphs(savefile=False, filepath=None):
    now = dt.datetime.now(pytz.timezone('America/New_York'))
    ayearago = now - relativedelta(years=1)

    upstairs = TempSeries.objects.get(name='Upstairs')
    upstairstemps = upstairs\
                        .tempreading_set.filter(timestamp__gte=ayearago)\
                        .order_by('timestamp')

    df = pd.DataFrame(list(upstairstemps.values()))
    df = df.set_index('timestamp')
    df.index = df.index.tz_convert('America/New_York')

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

        title = 'Temperature data going back %d day' % d
        if d > 1:
            title += 's'
        ax.set_title(title)

    for i in range(len(axes.flatten()) - 1):
        thisax = axes.flatten()[i]
        nextax = axes.flatten()[i + 1]
        nextlow, nexthigh = nextax.get_ylim()
        thisax.axvspan(nextlow, nexthigh, alpha=0.25, color='red')        

    fig.tight_layout()
    if savefile:
        if filepath is None:
            filepath = os.path.join(settings.STATIC_ROOT, 'images', 'fourgraphs.png')
        fig.savefig(filepath)
    return fig
