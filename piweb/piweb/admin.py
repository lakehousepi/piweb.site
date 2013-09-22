from django.contrib import admin
from piweb.models import IPReading, IPSeries, TempReading, TempSeries

class IPReadingAdmin(admin.ModelAdmin):
	pass

class IPSeriesAdmin(admin.ModelAdmin):
	pass

class TempReadingAdmin(admin.ModelAdmin):
	pass

class TempSeriesAdmin(admin.ModelAdmin):
	pass

admin.site.register(IPReading, IPReadingAdmin)
admin.site.register(IPSeries, IPSeriesAdmin)
admin.site.register(TempReading, TempReadingAdmin)
admin.site.register(TempSeries, TempSeriesAdmin)