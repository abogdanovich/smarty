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
import rrdtool

# Smarty main class
class Smarty:
    
    # configuration
    useNotifySend       = True
    useNotifySound      = False # not yet
    daemonTimeout       = 1 # timeout in seconds
    seconds             = 0 # timing in seconds
    tTiming             = 6 * 10 # timing in seconds
    rrd_base = '/home/nc/install/smarty/smarty-master/smarty_temperature.rrd'
    rrd_images = '/home/nc/install/smarty/smarty-master/temperature/'

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
        
    
    # get temperature sensors
    def checkTemperatureSensors(self):

	tdata1 = ow.Sensor('/28.B0E116040000').temperature #/28.B0E116040000 - topochnaya
	tdata2 = ow.Sensor('/28.AADE16040000').temperature #outdoor
	tdata3 = ow.Sensor('/28.B61C17040000').temperature #garage
	tdata4 = ow.Sensor('/28.DABF41040000').temperature #kitchen 1st floor
	tdata5 = 0 #reserved
	tdata6 = 0 #reserved
	tdata7 = 0 #reserved
	tdata8 = 0 #reserved
	tdata9 = 0 #reserved
	tdata10 = 0 #reserved
	
	logging.info('start data grub')
	logging.info('sensor topochnaya : ' + tdata1)
	logging.info('sensor outdoor : ' + tdata2)
	logging.info('sensor garage : ' + tdata3)
	logging.info('sensor kitchen 1st f : ' + tdata4)
	
	from rrdtool import update as rrd_update
	ret = rrd_update('/home/nc/install/smarty/smarty-master/smarty_temperature.rrd', 'N:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s' % (tdata1, tdata2, tdata3, tdata4, tdata5, tdata6, tdata7, tdata8, tdata9, tdata10));

	logging.info('END data grub')
	

	for sched in ['day' , 'week', 'month', 'year']:
	
	    if sched == 'week':
		period = 'w'
	    elif sched == 'day':
		period = 'd'
	    elif sched == 'month':
		period = 'm'
	    elif sched == 'year':
		period = 'y'
	    
	    ret = rrdtool.graph("/home/nc/install/smarty/smarty-master/temperature/temperature-%s.png" % (sched),
		 "--imgformat", "PNG",
		 "--width", "800",
		 "--height", "600",
		 "--start", "-1%s" % (period),
		 "--vertical-label", "T data",
		 "--title", "Temperature statistic",   
		 "-w 600",
		 "DEF:tdata1=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T1:AVERAGE",
		 "DEF:tdata2=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T2:AVERAGE",
		 "DEF:tdata3=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T3:AVERAGE",
		 "DEF:tdata4=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T4:AVERAGE",
		 "DEF:tdata5=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T5:AVERAGE",
		 "DEF:tdata6=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T6:AVERAGE",
		 "DEF:tdata7=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T7:AVERAGE",
		 "DEF:tdata8=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T8:AVERAGE",
		 "DEF:tdata9=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T9:AVERAGE",
		 "DEF:tdata10=/home/nc/install/smarty/smarty-master/smarty_temperature.rrd:T10:AVERAGE",
		 
		 "LINE2:tdata1#E39B1E:Topochnaya",
		 "GPRINT:tdata1:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata1:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata1:MAX:Max \: %2.1lf \\r",
		 
		 "LINE2:tdata2#E31E48:Outdoor ",
		 "GPRINT:tdata2:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata2:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata2:MAX:Max \: %2.1lf \\r",
		 
		 "LINE2:tdata3#1E1EE3:Garage ",
		 "GPRINT:tdata3:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata3:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata3:MAX:Max \: %2.1lf \\r",
		 
		 "LINE2:tdata4#B8E0AB:Kitchen ",
		 "GPRINT:tdata4:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata4:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata4:MAX:Max \: %2.1lf \\r",
		 
		 "LINE1:tdata5#B8E0AB:NA ",
		 "GPRINT:tdata5:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata5:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata5:MAX:Max \: %2.1lf \\r",
		 
		 "LINE1:tdata6#B8E0AB:NA ",
		 "GPRINT:tdata6:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata6:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata6:MAX:Max \: %2.1lf \\r",
		 
		 "LINE1:tdata7#B8E0AB:NA ",
		 "GPRINT:tdata7:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata7:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata7:MAX:Max \: %2.1lf \\r",
		 
		 "LINE1:tdata8#B8E0AB:NA ",
		 "GPRINT:tdata8:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata8:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata8:MAX:Max \: %2.1lf \\r",
		 
		 "LINE1:tdata9#B8E0AB:NA ",
		 "GPRINT:tdata9:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata9:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata9:MAX:Max \: %2.1lf \\r",
		 
		 "LINE1:tdata10#B8E0AB:NA ",
		 "GPRINT:tdata10:LAST:Now \: %2.1lf ",
		 "GPRINT:tdata10:MIN:Min \: %2.1lf ",
		 "GPRINT:tdata10:MAX:Max \: %2.1lf \\r")	
	
	
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
