from django.conf.urls import patterns, include, url
from django.conf import settings

from tastypie.api import Api
from piweb.api import (IPReadingResource, IPSeriesResource, TempReadingResource,
    TempSeriesResource)

from piweb import views
from debug_toolbar_line_profiler import profile_additional

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

    # Homepage
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^fourchartsstatic/$', views.FourChartsStaticView.as_view(), name='fourcharts_static'),
    url(r'^fourcharts/$', views.FourChartsView.as_view(), name='fourcharts'),

    url(r'^test/', views.TestView.as_view(), name='test'),
    url(r'^test2/', views.testview2, name='test2'),
    url(r'^test3/', views.testview3, name='test3'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
