#----------------------------------------------------------------------
# Copyright (c) 2009 Benito Jorge Bastida
# All rights reserved.
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#    o Redistributions of source code must retain the above copyright
#      notice, this list of conditions, and the disclaimer that follows.
#
#    o Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions, and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
#    o Neither the name of Digital Creations nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY DIGITAL CREATIONS AND CONTRIBUTORS *AS
#  IS* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#  PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL DIGITAL
#  CREATIONS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
#  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
#  DAMAGE.
#----------------------------------------------------------------------

from django.shortcuts import render_to_response
from django.conf import settings
from django.template import Template
from django.http import HttpResponseRedirect
from dajax.core import DajaxRequest
from django.views.decorators.cache import cache_control


def dajax_request(request, app_name, method):
    """
    dajax_request
    Uses DajaxRequest to handle dajax request.
    Return the apropiate json according app_name and method.
    """
    dr = DajaxRequest(request, app_name, method)
    return dr.process()

@cache_control(max_age=DajaxRequest.get_dajax_cache_control())
def js_core(request):
    """
    Return the dajax JS code according settings.DAJAX_FUNCTIONS registered functions.
    """
    def sanitize_js_names(name):
        name = name.rsplit('.',1)[0]
        return (name.replace('.','_'),name,)
    
    dajax_js_modules = [ sanitize_js_names(f.rsplit('.',1)[0]) for f in DajaxRequest.get_dajax_functions() ]
    dajax_js_functions_names = [ f.rsplit('.',1)[1] for f in DajaxRequest.get_dajax_functions() ]
    dajax_js_functions = zip(dajax_js_modules, dajax_js_functions_names)

    data = {'dajax_js_functions':dajax_js_functions, 'DAJAX_URL_PREFIX': DajaxRequest.get_media_prefix()}
    js_framework = DajaxRequest.get_dajax_js_framework().lower()
    
    try:
        return render_to_response('dajax/%s.dajax.core.js' % js_framework, data )
    except:
        if js_framework in DajaxRequest.get_dajax_available_js_frameworks():
            raise
        else:
            raise Exception("This JS Framework isn't available.")

def dajax_error(request):
    """
    Redirect if the url is invalid and settings.DAJAX_REDIRECT_ERROR exists.
    """
    if DajaxRequest.get_dajax_redirect_error() != None:
        return HttpResponseRedirect( DajaxRequest.get_dajax_redirect_error() )
    else:
        raise Exception("Dajax URL is not valid.")