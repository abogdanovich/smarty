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
owserver = 'localhost:4444'


#########################################################################
#Sensors functions
#########################################################################

def add_sensor(sensor_address, sensor_alias, sensor_family):
    
    try:
        sensor = Sensor.objects.get(address=sensor_address)
        sensor.delete()
    except Sensor.DoesNotExist:
        sensor= Sensor(address=sensor_address, alias=sensor_alias, active=0, locked=0, errors=0, family=sensor_family)
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
    
    sensors = Sensor.objects.all().filter(family=int(family)) #TODO: change active=1
    
    return sensors

def set_alert(sensor, priority, alert):
    
    try:
        alert= Alert(sensor=sensor, date=get_unix_datetime(), priority=priority, alert=alert)
        alert.save()
    except:
        alert = 0
        
    return alert


def save_monitor(message, status):

    try:
        monitor= Monitor(action=message, date=get_unix_datetime(), status=status)
        monitor.save()
    except:
        monitor = 0
        
    return monitor

def update_sensor_errors(sensor_address, flag):
    #errors = models.IntegerField(default=0) #count of errors | 2 errors - autoblock sensor + set alarm
    try:
        sensor = Sensor.objects.get(address=sensor_address)
        
        if flag == 0:
            sensor.errors = 0 # update errors and set 0
        else:
            sensor.errors += 1
                
            #check if we got 2 errors
            if check_block_sensor(sensor_address):
                #let's lock sensor
                sensor.locked = 1
                sid = set_alert(sensor.alias, 1, u"can't read sensor data")
                message = u"ошибка чтения датчика : %s" % (sensor.alias)
                print message
                save_monitor(message, sid.id)    
            
            #save sensor state    
            sensor.save()
            
    
    except Sensor.DoesNotExist:
        sensor = []

    return sensor


def check_block_sensor(sensor_address):
    
    try:
        sensor = Sensor.objects.get(address=sensor_address)
        if sensor.errors == 2:
            return True
    except Sensor.DoesNotExist:
        return False
    
    
def save_temperature(sensor, data):
    
    """
    sensor = models.CharField(max_length=30) #10.12AB23431211
    data = models.IntegerField() #temperature
    date = models.IntegerField() #date int format
    """
    
    try:
        sensor = Temperature(sensor=sensor, data=data, date=get_unix_datetime())
        sensor.save()
    except:
        sensor = []

    return sensor

def get_temperature():

    temp_data = Temperature.objects.all()

    return temp_data

def get_monitor_events():
    
    events = Monitor.objects.all()
    
    return events

def get_alert_events():
    
    alerts = Alert.objects.all()
    
    return alerts


"""
RRDTOOL


   path = os.path.realpath(os.path.dirname(__file__))
    dbname = "database.rrd"
    image = "image.png"
    fullpath = "%s/%s" % (path, dbname)
    fullimage = "%s/%s" % (path, image)
        
    if os.path.isfile(fullpath):

	ow.init('localhost:4444')
	sensors = ow.Sensor("/").sensorList()
	metric1 = sensors[0].temperature
	metric2 = sensors[1].temperature
	metric3 = sensors[2].temperature
	    
	ret = rrd_update(fullpath, 'N:%s:%s:%s' % (metric1, metric2, metric3))
	
	ret = rrdtool.graph(fullimage, "--start", "0", "--vertical-label=Temperature",
	     "-w 500",
	     "DEF:t1=/home/nc/tt/timecard/database.rrd:metric1:LAST",
	     "DEF:t2=/home/nc/tt/timecard/database.rrd:metric2:LAST",
	     "DEF:t3=/home/nc/tt/timecard/database.rrd:metric3:LAST",
	     "LINE2:t1#006633:metric 1\\r",
	     "GPRINT:t1:LAST:Average temperature\: %1.0lf ",
	     "COMMENT:\\n",
	     "LINE2:t2#0000FF:metric 2\\r",
	     "GPRINT:t2:LAST:Average temperature\: %1.0lf ",
	     "COMMENT:\\n",
	     "LINE2:t3#0073E6:metric 3\\r",
	     "GPRINT:t3:LAST:Average temperature\: %1.0lf",
	     "COMMENT:\\n")
	     	     
    else:
	
	ret = rrdtool.create(fullpath, "--step", "300",
	    "DS:metric1:GAUGE:600:U:U",
	    "DS:metric2:GAUGE:600:U:U",
	    "DS:metric3:GAUGE:600:U:U",
	    "RRA:LAST:0.5:1:576")

"""

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

