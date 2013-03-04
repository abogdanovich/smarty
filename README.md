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

**smarty network**
- 1-wire network (http://en.wikipedia.org/wiki/1-Wire)
- UTP 5 category cale (http://en.wikipedia.org/wiki/Category_5_cable)
*1-wire sensors*
- DALLAS DS18B20 - temperature sensor (http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf)
- DALLAS DS2408 - for relays controlling (http://www.maximintegrated.com/datasheet/index.mvp/id/3818)
- DALLAS DS2423 - counter for any impulse devices (http://datasheets.maximintegrated.com/en/ds/DS2423.pdf)
- DALLAS DS9490R - USB to 1-Wire Bridge Chip (master)

**server hardware|software**
- cubox (http://solid-run.com/cubox)
- Ubuntu 12.xx
**owfs**
- owfs-2.8p13 (http://sourceforge.net/projects/owfs/files/owfs/2.8p13/)

*owfs command lines*
- owserver: /opt/owfs/bin/owserver --tester=28,28,28,28,28,28,28,28,28,28,28,29,29 -p 4444 --error_level=9 --foreground --temperature_low=15 --temperature_high=25
- owhttpd: /opt/owfs/bin/owhttpd -s localhost:4444 -p 8888

**software**
- django web framework 1.3.1
- python-ow 2.8p13+dfsg1-5build1
- python 2.7.x
- xampp Linux 1.8.1 (http://www.apachefriends.org/en/xampp.html)

**external devices**
- SSR-25 DA Solid State Relay 25A Output 24V-380V (http://www.ebay.com/itm/271092328688?ssPageName=STRK:MEWAX:IT&_trksid=p3984.m1438.l2649)
- Electric Solenoid Valve For Water Air N/C 12V DC 1/2" Normally Closed (http://www.ebay.com/itm/130741056341?ssPageName=STRK:MEWAX:IT&_trksid=p3984.m1438.l2649)
- DHT11 Digital Temperature and Humidity Sensor (http://www.ebay.com/itm/220785316232?ssPageName=STRK:MEWAX:IT&_trksid=p3984.m1438.l2649)
- Electronic Flow Sensor Electronic Flow Meter 1-30L/M for solar water heater (http://www.ebay.com/itm/Electronic-Flow-Sensor-Electronic-Flow-Meter-1-30L-M-for-solar-water-heater-/261165339795?pt=LH_DefaultDomain_2&hash=item3cceaad493)
- current transformer SCT-013-030 0-30A Non-invasive AC current sensor Split Core Current Transformer (http://www.ebay.com/itm/SCT-013-030-0-30A-Non-invasive-AC-current-sensor-Split-Core-Current-Transformer-/181072923128?pt=US_Relays_Sensors&hash=item2a28c989f8)

**video monitoring**
- usb video stream (need for zoneminder connection if usb is used) (http://sourceforge.net/projects/mjpg-streamer/)
- fix for mjpg-streamer install (ubuntu center) (http://dineradmin.wordpress.com/2011/07/05/479/)
- mjpg-streamer cmd: sudo mjpg_streamer -i "input_uvc.so -r 320x240 -d /dev/video0 -f 30 -y -n" -o "output_http.so -p 8090"
- zoneminder (how to install: http://cleaner-lab.blogspot.com/2010/05/ubuntu-1004.html)

**NOOLIGHT**
- noolight controllers (http://habrahabr.ru/company/boxowerview/blog/168039/ http://www.noo.com.by/produkciya.html)

**PLANS**
- web design
- additional schemes \ loging description

*DAEMON*
- run cmd: python /home/alex/django/smarty/daemon/smartyDaemon.py start >> /tmp/smarty.log 2>&1




