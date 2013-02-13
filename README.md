Smarty
==============

Smarty Home System
--------------

**What smarty can control**
- get inside,outside temperature
- automatic lighting around the house
- automatic watering lawn
- inform user about all events (include alarms like high temperature or broken sensors)
- control water flow
- control energy consumption
- setting a schedule watering and outdoor lighting
- web\mobile access and system controlling
- monitoring the level of sewage
- video monitoring
- autosave system (all broken\blocked sensors will not touch the system)


**Software layer**

**network**
- 1-wire network (http://en.wikipedia.org/wiki/1-Wire)
*1-wire sensors*
- DALLAS DS18B20 (http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf)
- DALLAS DS2408 (http://www.maximintegrated.com/datasheet/index.mvp/id/3818)

**owfs**
- owfs-2.8p13 (http://sourceforge.net/projects/owfs/files/owfs/2.8p13/)
*owfs command lines*
- owserver: /opt/owfs/bin/owserver --tester=28,28,28,28,28,28,28,28,28,28,28,29,29 -p 4444 --error_level=9 --foreground --temperature_low=15 --temperature_high=25
- owhttpd: /opt/owfs/bin/owhttpd -s localhost:4444 -p 8888

**python plugins**
- python-ow 2.8p13+dfsg1-5build1  Dallas 1-wire support: Python bindings (Ubuntu repository)


**video monitoring**
- usb video stream (need for zoneminder connection if usb is used) (http://sourceforge.net/projects/mjpg-streamer/)
- fix for mjpg-streamer install (ubuntu center) (http://dineradmin.wordpress.com/2011/07/05/479/)
- mjpg-streamer cmd: sudo mjpg_streamer -i "input_uvc.so -r 320x240 -d /dev/video0 -f 30 -y -n" -o "output_http.so -p 8090"
- zoneminder (how to install: http://cleaner-lab.blogspot.com/2010/05/ubuntu-1004.html)

**django**
- django web framework
- python

**celery**
- cmd: python manage.py celeryd -v 2 -B -s celery -E -l INFO

**PLANS**

- 



