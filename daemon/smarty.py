# -*- coding: utf-8 -*-
#!/usr/bin/env python

import subprocess, os, pynotify, logging, tempfile, ConfigParser, sys
from datetime import datetime
import ow

class Smarty:
    useNotifySend       = True
    useNotifySound      = False #no yet
    daemonTimeout       = 0.5 #sec
    testvar             = 1

    def __init__(self):
        # log init
        logging.basicConfig(filename = tempfile.gettempdir() + '/smarty.log',
                            level = logging.DEBUG,
                            format = '%(asctime)s %(levelname)s: %(message)s',
                            datefmt = '%Y-%m-%d %I:%M:%S')
        logging.info('Daemon start')
        
        #ow init

        # start notify
        #self.fireNotify('Start!')

    def fireNotify(self, msg = '', title = 'Smarty Home System'):
        """
        Fire notify action
        """
        logging.info('Called fireNotify()')
        
        if (self.useNotifySend):
        
            #commands.getstatusoutput('notify-send -u "%s" -i "%s" "%s" "%s"' % (level, icon, title, msg))
            if pynotify.init('icon-summary-body'):
               
                pynotify.Notification(title, msg, self.getSystemIcon()).show()
            else:
                
                print 'Notify not supported. You need to install python-notify package first.'

        if (self.useNotifySound):
            # play sound event
            #if (self.useNotifySound):
            pass

    def getSystemIcon(self):
        """
        Get system icon path
        example: notification-power-disconnected
        """
        return ''

    def getLastCheckTime(self):
        """
        To simplicity, time of last modification of the current file is used as the time of last checking
        """
        lastCheckTime = os.path.getmtime(__file__)
        return datetime.fromtimestamp(lastCheckTime)

    def setLastCheckTime(self, time = None):
        """
        Set time of last checking -> touch file
        """
        #commands.getoutput('touch ' + __file__)
        #os.system('touch ' + __file__)
        subprocess.check_output('touch ' + __file__, shell=True)
        return self

    def getRepositoryPath(self):
        """
        Get repository path
        """
        return self.repositoryPath

    def getDaemonTimeout(self):
        """
        Get daemon checking timeout
        """
        return self.daemonTimeout

    def check(self, lastCheckTime = None, repositoryPath = None):
        """
        Get git log as string
        """
        logging.info('Called check()')
        #if (not lastCheckTime):
        #    lastCheckTime = self.getLastCheckTime()

        
        #only for test
        self.testvar += 1
        logging.info('testvar: %s', self.testvar)
        """

        if (countCommits > 0):
            logging.info('Test new changes: %s', countCommits)
            message += '...\n%s new commit(s)\n\n' % countCommits

            #self.fireNotify(message)
            #self.setLastCheckTime()
        """
        logging.info('End check()')
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