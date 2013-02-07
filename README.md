Smarty
==============

Smarty Home System
--------------

*Software list*

**owfs**
- owfs-2.8p13 (http://sourceforge.net/projects/owfs/files/owfs/2.8p13/)

**python**
- python-ow 2.8p13+dfsg1-5build1  Dallas 1-wire support: Python bindings (Ubuntu repository)

*owfs command lines*
- owserver: /opt/owfs/bin/owserver --tester=28,28,28,28,28,28,28,28,28,28,28,29,29 -p 4444 --error_level=9 --foreground --temperature_low=15 --temperature_high=25
- owhttpd: /opt/owfs/bin/owhttpd -s localhost:4444 -p 8888

*1-wire sensors*
- DALLAS DS18B20 (http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf)
- DALLAS DS2408 (http://www.maximintegrated.com/datasheet/index.mvp/id/3818)

*video monitoring*
- usb video stream (need for zoneminder connection if usb is used) (http://sourceforge.net/projects/mjpg-streamer/)
- fix for mjpg-streamer install (ubuntu center) (http://dineradmin.wordpress.com/2011/07/05/479/)
- mjpg-streamer cmd: sudo mjpg_streamer -i "input_uvc.so -r 320x240 -d /dev/video0 -f 30 -y -n" -o "output_http.so -p 8090"
- zoneminder (how to install: http://cleaner-lab.blogspot.com/2010/05/ubuntu-1004.html)

*usefull console commands*
- dmesg: check connected all devices
- lsusb: check connected usb devices

*django*
- django web framework
- python
