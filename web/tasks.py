# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# Django celery tasks
# author Alex Bogdanovich
# 2013 
#########################################################################

from celery.task import periodic_task
from celery.schedules import crontab

#########################################################################
#test func
@periodic_task(run_every=crontab(hour="*", minute="*/1", day_of_week="*"))
def test_print():
    n = 1+1
    print "celery test message % s" % (n)
    
#########################################################################
