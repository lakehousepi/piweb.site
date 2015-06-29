from tastypie.resources import ModelResource
from tastypie import fields
from piweb.models import IPReading, IPSeries, TempReading, TempSeries

class IPSeriesResource(ModelResource):
    class Meta:
        queryset = IPSeries.objects.all()
        resource_name = 'ipseries'

class IPReadingResource(ModelResource):
    ipseries = fields.ForeignKey(IPSeriesResource, 'ipseries')
    class Meta:
        queryset = IPReading.objects.all()
        resource_name = 'ipreading'
        order = ['timestamp', 'id', 'pk']

class TempSeriesResource(ModelResource):
    class Meta:
        queryset = TempSeries.objects.all()
        resource_name = 'tempseries'

class TempReadingResource(ModelResource):
    tempseries = fields.ForeignKey(TempSeriesResource, 'tempseries')
    class Meta:
        queryset = TempReading.objects.all()
        resource_name = 'tempreading'
        order = ['timestamp', 'id', 'pk']