from django.conf.urls import patterns, include, url

from tastypie.api import Api
from piweb.api import IPReadingResource, IPSeriesResource, TempReadingResource,
	TempSeriesResource

piweb_api = Api(api_name='piweb')
piweb_api.register(IPReadingResource())
piweb_api.register(IPSeriesResource())
piweb_api.register(TempReadingResource())
piweb_api.register(TempSeriesResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'piweb.views.home', name='home'),
    # url(r'^piweb/', include('piweb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

	# Tastypie API hookup
	url(r'^api/', include(piweb_api.urls)),
)
