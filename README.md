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

