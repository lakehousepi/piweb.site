from django.contrib import admin
from piweb.models import TempReading, TempSeries

class TempReadingAdmin(admin.ModelAdmin):
	pass

class TempSeriesAdmin(admin.ModelAdmin):
	pass

admin.site.register(TempReading, TempReadingAdmin)
admin.site.register(TempSeries, TempSeriesAdmin)