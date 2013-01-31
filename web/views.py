# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system module
# author Alex Bogdanovich
# 2013 
#########################################################################

#from timecard.models import 
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from timecard import utils
from django import template
#import socket
from datetime import date, timedelta, time
from django.core.exceptions import ObjectDoesNotExist
import pprint     # pretty print the lists
#import random
from django.http import HttpResponse
from django.template import loader, Context
#import csv
#import operator

#########################################################################

# my template loading section | modules

#template.add_to_builtins('timecard.templatetags.calendar')


#########################################################################


#########################################################################
#@utils.login_required
def main(request):
 
    d = dict(request=request)

    return render_to_response('web/main.html', d, context_instance=RequestContext(request))

#########################################################################