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
import pprint     
from django.http import HttpResponse
from django.template import loader, Context
import ow 
import utils

#########################################################################

def main(request):

    message = ""
    
    events = utils.get_monitor_events()
    
    alerts = utils.get_alert_events()
    
    temp_data = utils.get_temperature()
    
    
    d = dict(request=request, message=message, events=events, alerts=alerts, temp_data=temp_data)
    return render_to_response('web/main.html', d, context_instance=RequestContext(request))

#########################################################################

def sensors(request):

    slist = []
    message = ''
    sensors = []
    
    if request.method == 'POST' and 'add_sensor' in request.POST:
        #save sensor
        
        if utils.add_sensor(request.POST['sensor_address'], request.POST['sensor_alias'], int(request.POST['sensor_family']), request.POST['sensor_service']):        
            #d = dict(request=request, slist=slist, message=message)
            return redirect('/sensors/')
        else:
            message = 'sensor save error'        
            d = dict(request=request, slist=slist, message=message)
            return render_to_response('web/sensors.html', d, context_instance=RequestContext(request))    
    
    
    try:
        ow.init(utils.owserver)
        sensors = ow.Sensor('/').sensorList()
        
        for s in sensors:
            
            exist = utils.get_sensor(s.address)
            
            if int(s.family) == 28:
                if exist:
                    slist.append({'address': s.address, 'family': s.family, 'temperature': s.temperature, 'alias': exist.alias})
                else:
                    slist.append({'address': s.address, 'family': s.family, 'temperature': s.temperature})
                
            elif int(s.family) == 29:
                if exist:
                    slist.append({'address': s.address, 'family': s.family, 'PIO_ALL': s.PIO_ALL, 'alias': exist.alias})
                else:
                    slist.append({'address': s.address, 'family': s.family, 'PIO_ALL': s.PIO_ALL})
            
            else:
                slist.append({'address': s.address, 'family': s.family})
   
    except:
        message = 'OWserver error'
    
   
    
    d = dict(request=request, slist=slist, message=message, sensors=sensors)
    
    return render_to_response('web/sensors.html', d, context_instance=RequestContext(request))

#########################################################################

def settings(request):

    message = ''
    #utils.draw_timeline('poliv')
    #utils.draw_timeline('svet')
    
    controllers = utils.get_sensors(29) #controllers
    temp_data = utils.get_temperature()
    
    d = dict(request=request, message=message, controllers=controllers, temp_data=temp_data)
    return render_to_response('web/settings.html', d, context_instance=RequestContext(request))

#########################################################################