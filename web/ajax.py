# -*- coding: utf-8 -*-

#########################################################################
# Django settings for smarty project.
# author Alex Bogdanovich
# 2013 
#########################################################################

from dajax.core import Dajax
from dajaxice.core import dajaxice_functions
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from web import utils
import settings
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
import random
import datetime

#######################################################################

@dajaxice_register
def test(request, uid):
    dajax = Dajax()
    
    k = random.randint(0,1)
    
    if k:
	path = "%simages/button_off.jpg" % (settings.STATIC_URL)
    else:
	path = "%simages/button_on.jpg" % (settings.STATIC_URL)
    
    dajax.assign('#poliv_button','src',path)
    
    return dajax.json()

#######################################################################
