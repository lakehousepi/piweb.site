from tastypie.resources import ModelResource
from piweb.models import IPReading, IPSeries, TempReading, TempSeries

class IPReadingResource(ModelResource):
	class Meta:
		queryset = IPReading.objects.all()
		resource_name = 'ipreading'

class IPSeriesResource(ModelResource):
	class Meta:
		queryset = IPSeries.objects.all()
		resource_name = 'ipseries'

class TempReadingResource(ModelResource):
	class Meta:
		queryset = TempReading.objects.all()
		resource_name = 'tempreading'
		
class TempSeriesResource(ModelResource):
	class Meta:
		queryset = TempSeries.objects.all()
		resource_name = 'tempseries'