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

#########################################################################

def main(request):

    
    ow.init('localhost:4444')
    sensors = ow.Sensor('/').sensorList()
    
    slist = []
    for s in sensors:
        #print "%s %s" % (s.address, s.type)
        slist.append(s)
    
   
    d = dict(request=request, slist=slist)

    return render_to_response('web/main.html', d, context_instance=RequestContext(request))

#########################################################################