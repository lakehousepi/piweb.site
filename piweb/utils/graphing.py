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
from piweb.settings import STATIC_ROOT

def make_four_graphs():
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
    fig.savefig(os.path.join([STATIC_ROOT, 'fourgraphs.png']))
    return fig
