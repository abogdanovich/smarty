# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################

from django.db import models

#temperature sensors like DS18B20 read\write 
class Dsensor(models.Model): #Temperature sensor
    address = models.CharField(max_length=30) #10.12AB23431211
    alias = models.CharField(max_length=30) #10.12AB23431211 > we use WATER_OUTSIDE_1 for better usage
    status = models.IntegerField(default=0) # status 0 - disabled, 1 - active
    def __unicode__(self):
        return self.address
    
#temperature/humidity data sensors like DS18B20/HIH4000 read\write 
class Dsensor_data(models.Model): #Temperature/humidity sensors
    
    sensor = models.IntegerField() #sensor db id
    address = models.CharField(max_length=30) #10.12AB23431211
    data = models.FloatField()
    def __unicode__(self):
        return self.sensor    
    
#switch sensors like DS2408 read\write 
class Ssensor(models.Model): #Switch sensor
  
    address = models.CharField(max_length=30) #10.12AB23431211
    alias = models.CharField(max_length=30) #10.12AB23431211 > we use LIGHT_OUTSIDE_1 for better usage
    status = models.IntegerField(default=0) # status 0 - disabled, 1 - active
    def __unicode__(self):
        return self.address
#switch sensors data like DS2408 read\write 
class Ssensor_data(models.Model): #Temperature sensor
    
    sensor = models.IntegerField() #sensor db id
    address = models.CharField(max_length=30) #10.12AB23431211
    #POI_X usage and data storage 0 or 1
    pio_0 = models.IntegerField()
    pio_1 = models.IntegerField()
    pio_2 = models.IntegerField()
    pio_3 = models.IntegerField()
    pio_4 = models.IntegerField()
    pio_5 = models.IntegerField()
    pio_6 = models.IntegerField()
    pio_7 = models.IntegerField()

    def __unicode__(self):
        return self.sensor    

#log all important errors to inform user about them by email\sms etc...
class Alert(models.Model): #Alerts
    sensor = models.CharField(max_length=30) #sensor name NOT db id
    date = models.IntegerField()
    priority = models.IntegerField() #priority is set for warn user in critical situations
    alert = models.CharField(max_length=100) #alert message for user
    
    def __unicode__(self):
        return self.sensor

#monitor all actions in the smarty system
class Monitor(models.Model): #Alerts
    action = models.CharField(max_length=50) #smarty monitoring log for user review
    date = models.IntegerField()
    status = models.IntegerField() #0 - normal state (works fine), > 0 - error = alert id is used
    
    #status example:
    #Включения модуля автополив с 23.00 до 24.00 > state =0
    #Проверка работы модуля: вода есть  > state =0
    #Выключения модуля автополив с 23.00 до 24.00 > state =0
    #Проверка выключения модуля автополив с 23.00 до 24.00 > state = 16 - ALERT (id = 16): вода не выключена, возможна поломка запорного клапана!
    
    def __unicode__(self):
        return self.action
    
#celery run tasks each minute for all active sensors - but run only allowed actions - cases for summer\winter seasons...
class Calendar(models.Model): #Calendar for sensors
    sensor = models.IntegerField() #sensor id
    date = models.IntegerField() #yyyy-mm-dd-hh-mm(-ss)
    start_time = models.IntegerField() #start action time in int format like hh-mm
    end_time = models.IntegerField() #end action time in int format like hh-mm
    status = models.IntegerField(default=0) #1 - active, 0 - manually blocked (reason), Ssenso will not start until status = 0
    
    def __unicode__(self):
        return self.sensor
    
