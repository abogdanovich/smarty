# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################

from django.db import models

#temperature sensors like DS18B20 read\write 
class Sensor(models.Model): #all sensors
    
    address = models.CharField(max_length=30) #1012AB23431211
    alias = models.CharField(max_length=30) #1012AB23431211 > we use WATER_OUTSIDE_1 for better usage
    active = models.IntegerField(default=0) # 1 - active (working right now), 0 - sleep state
    locked = models.IntegerField(default=0) # 1 locked (can't work) by smarty or human - critical errors, 0 - can work - no errors
    errors = models.IntegerField(default=0) #count of errors | 2 errors - autoblock sensor + set alarm
    family = models.IntegerField() #28 or 29, 28 - DS18B20| 29 - DS2408
    service = models.CharField(max_length=30) #any additional service data
    
    def __unicode__(self):
        return self.address
    
#temperature/humidity data sensors like DS18B20/HIH4000 read\write 
class SensorData(models.Model): #Temperature/humidity sensors
    
    sensor = models.IntegerField() # senso id from Sensor model Class
    data = models.FloatField() #temperature, PIO 0 or 1
    date = models.IntegerField() #date int format
    
    def __unicode__(self):
        return self.sensor    

#log all important errors to inform user about them by email\sms etc...
class Alert(models.Model): #Alerts
    sensor = models.IntegerField() #sensor name NOT db id
    date = models.IntegerField()
    priority = models.IntegerField() #priority is set for warn user in critical situations
    alert = models.CharField(max_length=100) #alert message for user
    
    def __unicode__(self):
        return self.sensor

#monitor all actions in the smarty system
class Monitor(models.Model): #Alerts
    action = models.CharField(max_length=100) #smarty monitoring log for user review
    date = models.IntegerField()
    status = models.IntegerField() #0 - normal state (works fine), > 0 - error = alert id is used
    
    def __unicode__(self):
        return self.action
    
#calendar for sensors runs
class Calendar(models.Model): #Calendar for sensors
    sensor = models.IntegerField() #sensor id
    
    #from '2013-01-01 00:00' (jan 2013) = 1357020000 till '2013-02-01 00:00' (feb 2013) 1362117600 (1 month)
    start_date = models.IntegerField() #yyyy-mm-dd-hh-mm(-ss) 
    end_date = models.IntegerField() #yyyy-mm-dd-hh-mm(-ss)
    
    #from '00:00' = 2208967200 = till 2208960000 '02:00' = 2 hours of sensor work
    start_time = models.IntegerField() #start action time in int format like hh-mm
    end_time = models.IntegerField() #end action time in int format like hh-mm
    locked = models.IntegerField(default=0) #1 - locked, 0 - manually blocked (reason), Sensor will not start until status = 0
    
    def __unicode__(self):
        return self.sensor
    
#class events to sync daemon with clients and push all HUMAN actions into daemon to make action 
class DaemonEvents(models.Model):
    sensor = models.IntegerField() #1012AB23431211
    
    action = models.IntegerField() # 1 - switch ON, 0 - switch OFF - like sensor.PIO_1 = action
    date = models.IntegerField() #yyyy-mm-dd-hh-mm(-ss)
    status = models.IntegerField() #0 - completed (isn't active), 1 - ready for action
    
    def __unicode__(self):
        return self.sensor
    
