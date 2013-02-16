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
import ow
import PIL
import Image, ImageDraw
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
    
    try:
        sensor = Temperature(sensor=sensor, data=data, date=get_unix_datetime())
        sensor.save()
        print "saved temperature data"
    except:
        sensor = []

    return sensor

def save_pio(sensor, data):
    
    try:
        spio = data.split(",")
        #spio_1 = spio[0:4] #канализация 1 (4 датчика)
        #spio_2 = spio[4:8] #канализация 1 (4 датчика)

        s = Controller(sensor=sensor, pio_0=spio[0], pio_1=spio[1], pio_2=spio[2], pio_3=spio[3], pio_4=spio[4], pio_5=spio[5], pio_6=spio[6], pio_7=spio[7], date=get_unix_datetime())
        s.save()
        print "saved PIO DATA"
    except:
        s = []

    return s
        

def get_temperature():

    sensors = Sensor.objects.all().filter(family=28)
    temp_data = []
    
    for s in sensors:
        sensor_data = Temperature.objects.filter(sensor=s.address).order_by('-date')[:1]
        #print sensor_data
        if sensor_data:
            date = convert_unix_date('all', sensor_data[0].date)
            temp_data.append({'sensor': s.alias, 'date': date, 'data': sensor_data[0].data})
        else:
            #date = convert_unix_date('all', sensor_data[0].date)
            temp_data.append({'sensor': s.alias, 'date': 0, 'data': 0})
            

    return temp_data

def get_piodata():

    sensors = Sensor.objects.all().filter(family=29)
    temp_data = []
    
    for s in sensors:
        sensor_data = Controller.objects.filter(sensor=s.address).order_by('-date')[:1]
        #print sensor_data
        if sensor_data:
            date = convert_unix_date('all', sensor_data[0].date)
            temp_data.append({'sensor': s.alias, 'date': date, 'pio_0': sensor_data[0].pio_0, 'pio_1': sensor_data[0].pio_1, 'pio_2': sensor_data[0].pio_2, 'pio_3': sensor_data[0].pio_3, 'pio_4': sensor_data[0].pio_4, 'pio_5': sensor_data[0].pio_5, 'pio_6': sensor_data[0].pio_6, 'pio_7': sensor_data[0].pio_7})
        else:
            temp_data.append({'sensor': s.alias, 'date': 0, 'pio_0': 0, 'pio_1': 0, 'pio_2': 0, 'pio_3': 0, 'pio_4': 0, 'pio_5': 0, 'pio_6': 0, 'pio_7': 0})

    return temp_data


def get_monitor_events():
    
    e = Monitor.objects.all().order_by('-date')[:10]
    events = []
    for event in e:
        date = convert_unix_date('all', event.date)
        events.append({'action': event.action, 'date': date, 'status': event.status})
    
    return events

def get_alert_events():
    
    a = Alert.objects.all().order_by('-date')[:10]
    alerts = []
    for alert in a:
        date = convert_unix_date('all', alert.date)
        alerts.append({'sensor': alert.sensor, 'date': date, 'priority': alert.priority, 'alert': alert.alert})
    
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

