# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################


from web.models import Sensor, SensorData, Alert, Monitor, Calendar
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
import ow
import PIL
import Image, ImageDraw
import random
#########################################################################

#Global settings

TIMEZONE = "Europe/Minsk"
ADMIN_EMAIL = "abogdanovich@minsk.ximxim.com"
owserver = 'localhost:4444'


#########################################################################
#Sensors functions
#########################################################################

def add_sensor(sensor_address, sensor_alias, sensor_family, sensor_extra):
    
    try:
        sensor = Sensor.objects.get(address=sensor_address)
        sensor.delete()
        sensor= Sensor(address=sensor_address, alias=sensor_alias, active=0, locked=0, errors=0, family=sensor_family, extra=sensor_extra)
        sensor.save()
    except Sensor.DoesNotExist:
        sensor= Sensor(address=sensor_address, alias=sensor_alias, active=0, locked=0, errors=0, family=sensor_family, extra=sensor_extra)
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
def get_sensors(family):
    
    if family == 'all':
        sensors = Sensor.objects.all()
    else:
        sensors = Sensor.objects.all().filter(family=int(family)) #TODO: change active=1
    
    return sensors

def set_alert(sensor, priority, alert):
    
    try:
        alert= Alert(sensor=sensor, date=get_unix_datetime(), priority=priority, alert=alert)
        alert.save()
    except:
        alert = 0
        
    return alert

    
def get_temperature():

    sensors = Sensor.objects.all().filter(family=28)
    temp_data = []
    
    for s in sensors:
        sensor_data = SensorData.objects.filter(sensor=s.address).order_by('-date')[:1]
            
        if s.service:
            coords = s.service.split("|")
            x = random.randint(10,600)#coords[0]
            y = random.randint(10,600)#coords[1]
        else:
            x = random.randint(10,600)#0
            y = random.randint(10,600)#0
        
        if sensor_data:
            date = convert_unix_date('all', sensor_data[0].date)
            temp_data.append({'sensor': s.alias, 'date': date, 'data': round(sensor_data[0].data, 1), 'x': x, 'y': y})
        else:
            temp_data.append({'sensor': s.alias, 'date': 0, 'data': 0, 'x': x, 'y': y})

    return temp_data


def get_monitor_events():
    
    e = Monitor.objects.all().order_by('-date')[:20]
    events = []
    for event in e:
        date = convert_unix_date('time', event.date)
        events.append({'action': event.action, 'date': date, 'status': event.status})
    
    return events

def get_alert_events():
    
    a = Alert.objects.all().order_by('-date')[:10]
    alerts = []
    for alert in a:
        date = convert_unix_date('all', alert.date)
        alerts.append({'sensor': alert.sensor, 'date': date, 'priority': alert.priority, 'alert': alert.alert})
    
    return alerts


#########################################################################
# other utils
#########################################################################


#########################################################################

# PIL office statistic: browsers
  
def draw_timeline(sensor):
    #starttime, endtime, sensor
    #sensor = poliv, svet
    #starttime - from day
    #endtime - end day
    
    filename = "%stimeline%s.jpg" % (settings.MEDIA_ROOT, sensor)
    
    pic_size = 380,60
    size = 370,50
        
    im = Image.new('RGB', pic_size)
    draw = ImageDraw.Draw(im)
    #draw.rectangle((0,0,pic_size[0]-1,pic_size[1]-1), fill="#000000")
    draw.rectangle((0,0,pic_size[0],pic_size[1]), fill="#FFFFFF")
    
    #draw.line((5, 220, 5, 5), fill="#707070", width=1)
    #draw.line((5, 220, 520, 220), fill="#707070", width=1)
    if sensor == 'poliv':
        draw.line((1,10,370, 10), fill="blue", width=1)
    else:
        draw.line((1,10,370, 10), fill="red", width=1)
    
    im.save(filename, quality=100)  
  
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
    else:
        dt_obj = datetime.datetime.fromtimestamp(timestamp)
        return pytz.timezone(TIMEZONE).fromutc(dt_obj).strftime("%Y-%m-%d %H:%M")

#########################################################################

