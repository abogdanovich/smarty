# -*- coding: utf-8 -*-
#!/usr/bin/env python

#########################################################################
# Smarty home system DAEMON module
# author Alex Bogdanovich
# 2013 
#########################################################################

import subprocess, os, pynotify, logging, tempfile, ConfigParser, sys
import datetime
import time
import ow
import MySQLdb

# Smarty main class
class Smarty:
    
# configuration
    useNotifySend       = True
    useNotifySound      = False # not yet
    daemonTimeout       = 1 # timeout in seconds
    seconds             = 0 # timing in seconds
    tTiming             = 5 * 1 # 5 * 60

    #init 
    def __init__(self):
        # log init
        logging.basicConfig(filename = tempfile.gettempdir() + '/smarty.log', format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)

        logging.info('Daemon start')
        
        # ow init
        try: 
            logging.info('1-wire network init owserver')
            ow.init('localhost:4444')
        except:
            logging.error('1-wire network init')
            sys.exit(0)
        
#----------------------------------------------------
    
    def DB_SELECT(self, TABLE, PARAM = '', SIGN = '', VALUE = ''):
      
      numrows = 0
      records = []
      
      if TABLE != '':
          try:
      
              conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="smarty", charset='utf8') # name of the data base
              cursor = conn.cursor()
              
              if PARAM != '' and SIGN != '' and VALUE != '':
              
                  cursor.execute("SELECT * FROM %s WHERE %s %s %s" % (TABLE, PARAM, SIGN, VALUE))
              else:
                  
                  cursor.execute("SELECT * FROM %s" % (TABLE))
              
              #get selected row count
              numrows = int(cursor.rowcount)
              
              #fetch table records
              records = cursor.fetchall()
      
          except IOError, e:
              #TODO: log db error instead of print
              print "Error %d: %s" % (e.args[0],e.args[1])
              
          finally:
              if cursor:
                  cursor.close()
              
              if conn:
                  conn.close()
      
      else:
          print 'need to select db table name!'
          
      return numrows, records
      
#----------------------------------------------------

    def DB_UPDATE(self, TABLE, PARAM = '', VALUE = '', SID = ''):
        
        flag = False
        #SID = db address field instead of id table record
        
        if TABLE != '':
            try:
    
                conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="smarty", charset='utf8') # name of the data base
                cursor = conn.cursor()
                
                if PARAM != '' and VALUE != '' and SID != '':
                    cursor.execute("UPDATE %s SET %s='%s' WHERE address='%s'" % (TABLE, PARAM, VALUE, SID))
                    conn.commit()
                    flag = True
        
            except IOError, e:
                #TODO: log db error instead of print
                print "Error %d: %s" % (e.args[0],e.args[1])
                
            finally:
                if cursor:
                    cursor.close()
                
                if conn:
                    conn.close()
        
        else:
            #TODO: log db error instead of print
            print 'TABLE name is empty'
            
        return flag

#----------------------------------------------------

    
    def getUnixDatetime(self):

        dt = datetime.datetime.utcnow()
        sdate = dt.strftime('%Y-%m-%d %H:%M')

        return int(time.mktime(time.strptime(sdate, "%Y-%m-%d %H:%M")))
    

#----------------------------------------------------
  
    
    # get temperature sensors
    def checkTemperatureSensors(self):
        
        slist = []

        slist = self.DB_SELECT('web_sensor', 'family', '=', 28)
        

        if slist[0] > 0:
        
            for s in slist[1]:

                s_temp = ow.Sensor(str('/' + s[1])).temperature
                logging.info('sensor ' + s[1] + ' data: ' + s_temp)
                #update DB with a real new temp data
                #self.DB_UPDATE('web_sensor', 'data', s_temp, s[1])
                
        else:
            logging.error('no sensors in db!')
        
        return self
    
#----------------------------------------------------    

    # Get daemon checking timeout

    def getDaemonTimeout(self):
        
        return self.daemonTimeout

#----------------------------------------------------

    # check every seconds 
    def check(self):
        
        if self.seconds >= self.tTiming:
            self.seconds = 1
            self.checkTemperatureSensors()
            
        else:
            self.seconds += 1
        
        logging.info("seconds: %s" % self.seconds)

        return self

#----------------------------------------------------
if __name__ == '__main__':
    c = Smarty()
    c.check()
#----------------------------------------------------
    
#trach code 
    
    
"""

        #s = ow.Sensor('/293EA141E1FC6712').PIO_ALL
        #logging.info("Controller data: %s" % s)
        
        #check controllers state
        #self.getControllerStates(s)
        

# -*- coding: utf-8 -*-


import MySQLdb

try:
    con = MySQLdb.connect(host="localhost", user="root", passwd="5213", db="test")
    cur = con.cursor()
    cur.execute('SET NAMES `utf8`')
    cur.execute('SELECT `name` FROM `city` ORDER BY `name` DESC')
    result = cur.fetchall()
    for row in result:
        print(row[0])        
except MySQLdb.Error:
    print(db.error())

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