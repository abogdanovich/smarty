# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################

from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('web.views',
    # Examples:
    # url(r'^$', 'smarty.views.home', name='home'),
    
    url(r'^$', 'main'),
    url(r'^sensors', 'sensors'),
    url(r'^video', 'video'),
    url(r'^settings', 'settings'),
    #url(r'^login', include('login')),
    #url(r'^logout', include('logout')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
