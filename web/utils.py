# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################


from web.models import Sensor, Temperature, Controller, Alert, Monitor, Calendar
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, send_mass_mail
import calendar
import datetime
import time
import pytz
import pprint  
import os
import logging
#########################################################################

#Global settings

TIMEZONE = "Europe/Minsk"
ADMIN_EMAIL = "abogdanovich@minsk.ximxim.com"


#########################################################################
#Sensors functions
#########################################################################

def add_sensor(sensor_address, sensor_alias):
    
    flag = 0

    try:
        sensor = Sensor.objects.get(address=sensor_address)
        sensor.delete()
    except Sensor.DoesNotExist:
        sensor= Sensor(address=sensor_address, alias=sensor_alias, active=0, locked=0)
        sensor.save()

    return sensor.id

#get sensor object
def get_sensor(sensor_address):
    
    try:
        sensor = Sensor.objects.get(address=sensor_address)
    except Sensor.DoesNotExist:
        sensor = []
    
    return sensor

#get sensor object
def get_sensors():
    sensors = Sensor.objects.all()
    
    return sensors

#########################################################################
# other utils
#########################################################################

# seconds into hh:mm converter

def convert_seconds(secs):

    total   = secs
    hours   = total / 3600
    total   = total - (hours * 3600)
    mins    = total / 60

    return "%02d:%02d" % (hours, mins)

#########################################################################

# convert str datetime into UNIX (int) format

def get_unix_strdtime(sel, dtime):
    if sel == 'date':
        return int(time.mktime(time.strptime(dtime, "%Y-%m-%d")))
    elif sel == 'time':
        return int(time.mktime(time.strptime(dtime, "%H:%M")))
    else:
        return int(time.mktime(time.strptime(dtime, "%Y-%m-%d %H:%M")))


#########################################################################

# convert UTCNOW datetime into UNIX format

def get_unix_datetime():

    dt = datetime.datetime.utcnow()
    sdate = dt.strftime('%Y-%m-%d %H:%M')

    return int(time.mktime(time.strptime(sdate, "%Y-%m-%d %H:%M")))
    
#########################################################################

# convert UNIX timestamp format into datetime

def convert_unix_date(sel, timestamp):
    if sel == 'date':
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
	return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%Y-%m-%d")
    elif sel == 'time':
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%H:%M")
    elif sel == 'stattime':
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%H")
    else:
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%Y-%m-%d %H:%M")

#########################################################################

