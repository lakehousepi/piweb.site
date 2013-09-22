from tastypie.resources import ModelResource
from piweb.models import TempReading

class TempReadingResource(ModelResource):
	class Meta:
		queryset = TempReading.objects.all()
		resource_name = 'tempreading'