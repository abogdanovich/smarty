# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django import template
from datetime import date, timedelta, time
from django.core.exceptions import ObjectDoesNotExist
import pprint     # pretty print the lists
from django.http import HttpResponse
from django.template import loader, Context
#need to use 2.8p20 to exclude sensors reading problem
import ow 
import utils

#########################################################################

def main(request):

    slist = []
    error = ''
    
    try:
        ow.init('localhost:4444')
        sensors = ow.Sensor('/').sensorList()
        for s in sensors:
            slist.append(s)
    except:
        error = 'OWFS  Network problems'
    
    d = dict(request=request, slist=slist, error=error)
    return render_to_response('web/main.html', d, context_instance=RequestContext(request))

#########################################################################

def sensors(request):

    error = ''
    d = dict(request=request, error=error)
    return render_to_response('web/sensors.html', d, context_instance=RequestContext(request))

#########################################################################

def video(request):

    error = ''
    d = dict(request=request, error=error)
    return render_to_response('web/video.html', d, context_instance=RequestContext(request))

#########################################################################

def settings(request):

    error = ''
    d = dict(request=request, error=error)
    return render_to_response('web/settings.html', d, context_instance=RequestContext(request))

#########################################################################