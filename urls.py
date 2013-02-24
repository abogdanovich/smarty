# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smarty.views.home', name='home'),
    
    url(r'^', include('web.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_ROOT+'/static'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_ROOT+'/media'}),
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
