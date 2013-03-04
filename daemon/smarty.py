# -*- coding: utf-8 -*-
#!/usr/bin/env python

import subprocess, os, pynotify, logging, tempfile, ConfigParser, sys
from datetime import datetime
import ow

class Smarty:
    useNotifySend       = True
    useNotifySound      = False #no yet
    daemonTimeout       = 1 #sec
    testvar             = 1
    

    def __init__(self):
        # log init
        logging.basicConfig(filename = tempfile.gettempdir() + '/smarty.log',
                            level = logging.DEBUG,
                            format = '%(asctime)s %(levelname)s: %(message)s',
                            datefmt = '%Y-%m-%d %I:%M:%S')
        logging.info('Daemon start')
        
        #ow init
        logging.info('1-wire network init')
        ow.init('localhost:4444')

        # start notify
        
    def saveTemperatureSensors(self):
        
        logging.info('Call saveTemperatureSensors()')
        
        return self
        
    def getSewageLoading(self, pio=''):
        
        pioList = []
        s1List = []
        s2List = []
        pioList = pio.split(",")
        
        s1List = pioList[0:4]
        s2List = pioList[4:8]
        
        logging.info('pio list: %s' % pio)
        
        loading1 = 0
        loading2 = 0
        
        for p in s1List:
            if int(p) == 1:
                loading1 += 1
        
        loading1 *= 25
        
        for p in s2List:
            if int(p) == 1:
                loading2 += 1
        
        loading2 *= 25
        
        return loading1,loading2
    
    def getControllerStates(self, pio=''):
        
        pioList = pio.split(",")
        
        if int(pioList[0]) == 1:
            #water outside is on
            logging.info('watering lawn is ON')
        else:
            logging.info('watering lawn is OFF')
            
            
        if int(pioList[1]) == 1:
            #water outside is on
            logging.info('automatic lighting is ON')
        else:
            logging.info('automatic lighting is OFF')
            
        if int(pioList[3]) == 1:
            #water outside is on
            logging.info('Door #1 is open')
        else:
            logging.info('Door #1 is closed')
        
        if int(pioList[4]) == 1:
            #water outside is on
            logging.info('wicket Door is open')
        else:
            logging.info('wicket Door is closed')
        
        
        if int(pioList[4]) == 1:
            #water outside is on
            logging.info('garage Doors is open')
        else:
            logging.info('garage Doors is closed')
            
        if int(pioList[5]) == 1:
            #water outside is on
            logging.info('home garage Doors is open')
        else:
            logging.info('home garage Doors is closed')
        
        
        return self  

    def getDaemonTimeout(self):
        """
        Get daemon checking timeout
        """
        return self.daemonTimeout

    def check(self):
        
        if self.testvar >= 240:
            self.testvar = 1
            self.saveTemperatureSensors()
        else:
            self.testvar += 1
        
        s = ow.Sensor('/2867C6697351FF68').temperature
        logging.info("Sensor data: %s" % s)
        
        s = ow.Sensor('/284AEC29CDBAAB95').temperature
        logging.info("Sensor data: %s" % s)
        
        s = ow.Sensor('/28F2FBE3467CC278').temperature
        logging.info("Sensor data: %s" % s)
        
        s = ow.Sensor('/2854F81BE8E78D50').temperature
        logging.info("Sensor data: %s" % s)
        
        s = ow.Sensor('/28765A2E63339F10').temperature
        logging.info("Sensor data: %s" % s)
        
        s = ow.Sensor('/293E017E97EADC99').PIO_ALL
        logging.info("Controller data: %s" % s)
        
        loading = self.getSewageLoading(s)
        
        s = ow.Sensor('/293EA141E1FC6712').PIO_ALL
        logging.info("Controller data: %s" % s)
        
        #check controllers state
        self.getControllerStates(s)
        
        logging.info('Канализация 1: %s | Канализация 2: %s ' % (loading[0], loading[1]))
        
        
        return self

if __name__ == '__main__':
    c = Smarty()
    c.check()
    
    
    
    
    
"""
# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# Django celery tasks
# author Alex Bogdanovich
# 2013 
#########################################################################

from celery.task import periodic_task
from celery.schedules import crontab
import utils
import ow

#########################################################################

#########################################################################
# task1 опрос датчиков температуры, влажности воздуха, датчика осадков
# period = всегда каждые 5 минут
# сохранение данных, построение графиков температуры, влажности
#########################################################################
# for test - опрос каждую минуту

@periodic_task(ignore_result=True, run_every=crontab(hour="*", minute="*/1", day_of_week="*"))
def get_temperature():
    # берем все датчики и по очереди каждого опрашиваем
    sensors = utils.get_sensors(28) #get only 28 family type sensors

    #заносим в монитор события опроса
    #message = u"получение температу"
    #utils.save_monitor(message, 0)
    
    ow.init(utils.owserver)
    
    for s in sensors:
	try:
	    s_temp = ow.Sensor(str('/' + s.address)).temperature
	    # если было накопление error на сенсоре- обнуляем его в случае нормальной работы
	    
	    if s_temp:
		if utils.save_temperature(s.address, s_temp):
		    message = u"сохранения данных: %s" % (s.alias)
		    #print message
		    utils.save_monitor(message, 0)
		else:
		    message = u"ошибка сохранения данных: %s" % (s.alias)
		    #print message
		    utils.save_monitor(message, 0)
		    
	except:
	    # если датчик не отвечает - увеличиваем поле errors заносим alarm
	    utils.update_sensor_errors(s.address, 1) #sensor error! set+1 for sensor errors

    #message = u"опрос датчиков температуры завершен"
    utils.save_monitor(message, 0)
    
#########################################################################

# TODO: сделать возможно управлять поливом и освещением по месячно, динамично меняя через web сайт
# тогда система будет каждую минуту будет проверять в базе на дату и время (можно ли это сделать)

# TODO: control sensors errors >= 2 to lock (do not accumulate them in errors field)


#########################################################################
# task2 опрос датчиков уровня канализации, 2 канализации по 4 положения в каждом = 8 ног
# датчик DS2408 POI_0..POI_7
# period = всегда каждые 5 минут
# сохранение данных в зависимости от полученных данных, если изменилось
# состояние от предыдущего - 1 положение = 25% заполнение ёмкости  
@periodic_task(ignore_result=True, run_every=crontab(hour="*", minute="*/5", day_of_week="*"))
def get_sewage():
    # берем все датчики и по очереди каждого опрашиваем
    sensor = utils.get_sensor(str('293EA141E1FC6712')) #get only 28 family type sensors

    #заносим в монитор события опроса
    #message = u"программа получения уровня канализации стратовала"
    #utils.save_monitor(message, 0)
    
    ow.init(utils.owserver)
    
    try:
	#print sensor.address
	data = ow.Sensor(str('/' + sensor.address)).PIO_ALL
	#print s_sewage
	
	# если было накопление error на сенсоре- обнуляем его в случае нормальной работы
	
	if data:
	    if utils.save_pio(sensor.address, data):
		message = u"сохранения данных: %s" % (sensor.alias)
		#print message
		utils.save_monitor(message, 0)
	    else:
		message = u"ошибка сохранения данных: %s" % (sensor.alias)
		#print message
		utils.save_monitor(message, 0)
		
    except:
	# если датчик не отвечает - увеличиваем поле errors заносим alarm
	utils.update_sensor_errors(sensor.address, 1) #sensor error! set+1 for sensor errors

    #message = u"программа получения уровня канализации ЗАВЕРШЕНА"
    #utils.save_monitor(message, 0)

#########################################################################

#########################################################################
# task3 включение автополива с проверкой:
# 1. можно ли поливать (анализ датчика осадков)
# 2. проверка - есть ли вода - тогда включаем и проверяем что клапана включились
# датчик DS2408 POI_0..POI_7
#########################################################################

#########################################################################
# task4 выключение автополива с проверкой:
# проверка выключена ли вода
# датчик DS2408 POI_0..POI_7
#########################################################################

#########################################################################
# task5 включение наружного освещения с проверкой на датчик освещения (достаточно ли темно)
# датчик DS2408 POI_0..POI_7
# TODO: проверка включения освещения через датчик освещение или напряжение
#########################################################################

#########################################################################
# task6 выключение наружного освещения с проверкой на датчик освещения (достаточно ли темно)
# проверка датчика освещения (действительно ли выключилось освещение)
# датчик DS2408 POI_0..POI_7
# TODO: проверка включения освещения через датчик освещение или напряжение
#########################################################################

"""