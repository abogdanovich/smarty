# -*- coding: utf-8 -*-

#########################################################################
# Django settings for smarty project.
# author Alex Bogdanovich
# 2013 
#########################################################################

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from smarty import utils
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
    
    #path = "%simages/button_off.jpg" % (settings.STATIC_URL)
    dajax.alert("test is OK")
    #dajax.assign('#poliv_button','src',path)
    
    return dajax.json()

#######################################################################
