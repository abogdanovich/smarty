# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################


#from timecard.models import User, UserTime, UserPost, UserPostComment, CalendarDaysOff, UserModule, UserMissedHours, Boss_notice, User_duty, Projects, UserProjectAssignments
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, send_mass_mail
import calendar
import datetime
import time
import pytz
#import Image, ImageFilter, ImageDraw
#import operator
#import itertools
import pprint     # pretty print the lists
import os
#import random
import logging
#from django.db.models import Q
#########################################################################

#Global settings

TIMEZONE = "Europe/Minsk"
ADMIN_EMAIL = "abogdanovich@minsk.ximxim.com"

#########################################################################
