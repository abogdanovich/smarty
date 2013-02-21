# -*- coding: utf-8 -*-
#/usr/bin/python

#import os, sys

#sys.path.append("/home/alex/django/smarty/")

# В python path добавляется директория проекта
#dn = os.path.dirname
#PROJECT_ROOT = os.path.abspath( dn(dn(__file__)) )
#DJANGO_PROJECT_ROOT = os.path.join(PROJECT_ROOT, 'apps')
#sys.path.append(DJANGO_PROJECT_ROOT)

# Установка файла настроек
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Запуск wsgi-обработчика
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()


import os
import sys

sys.path.insert(0, '/home/alex/django/smarty')

import settings

import django.core.management
django.core.management.setup_environ(settings)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

