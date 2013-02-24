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

import os
from django.conf import settings
from dajax.core import Dajax

try:
    from django.utils import importlib
    DAJAX_MODERN_IMPORT = True
except:
    DAJAX_MODERN_IMPORT = False

class DajaxRequest(object):
    """
    DajaxRequest Class.
    """
    def __init__(self, request, app_name, method):
        self.app_name = app_name
        self.method = method
        self.request = request
        
        self.project_name = os.environ['DJANGO_SETTINGS_MODULE'].split('.')[0]
        self.module = "%s.ajax" % self.app_name
        self.full_name = "%s.%s" % (self.module,self.method,)
    
    def is_callable(self):
        """
        Return if the request function was registered.
        """
        if self.full_name in settings.DAJAX_FUNCTIONS:
            return True
        return False
        
    @staticmethod
    def get_dajax_available_js_frameworks():
        return ('prototype','jquery','mootools','dojo',)
        
    @staticmethod
    def get_dajax_error_callback():
        return getattr(settings, 'DAJAX_ERROR_CALLBACK', None)
        
    @staticmethod
    def get_media_prefix():
        return getattr(settings, 'DAJAX_MEDIA_PREFIX', "dajax")
        
    @staticmethod
    def get_dajax_functions():
        return getattr(settings, 'DAJAX_FUNCTIONS', ())
        
    @staticmethod
    def get_dajax_js_framework():
        return getattr(settings, 'DAJAX_JS_FRAMEWORK', "Prototype")
    
    @staticmethod
    def get_dajax_redirect_error():
        return getattr(settings, 'DAJAX_REDIRECT_ERROR', None )
    
    @staticmethod
    def get_dajax_debug():
        return getattr(settings, 'DAJAX_DEBUG', True )
    
    @staticmethod
    def get_dajax_cache_control():
        if settings.DEBUG:
            return 0
        return getattr(settings, 'DAJAX_CACHE_CONTROL', 5 * 24 * 60 * 60 )
    
    def get_ajax_function(self):
        """
        Return a callable ajax function.
        This function should be imported according the Django version.
        """
        if DAJAX_MODERN_IMPORT:
            return self.__modern_get_ajax_function()
        else:
            return self.__old_get_ajax_function()
    
    def __old_get_ajax_function(self):
        """
        Return a callable ajax function.
        This function doesn't uses django.utils.importlib
        """
        
        self.module_import_name = "%s.%s" % ( self.project_name, self.module)   
        try:
            return self.__old_import()
        except:
            self.module_import_name = self.module
            return self.__old_import()
    
    def __old_import(self):
        """
        Import this.module_import_name 
        This function doesn't uses django.utils.importlib
        """
        mod = __import__(self.module_import_name , None, None, [self.method])
        return mod.__getattribute__(self.method)
        
    def __modern_get_ajax_function(self):
        """
        Return a callable ajax function.
        This function uses django.utils.importlib
        """
        self.module_import_name = "%s.%s" % ( self.project_name, self.module )
        try:
            return self.__modern_import()
        except:
            self.module_import_name = self.module
            return self.__modern_import()
    
    def __modern_import(self):
        from django.utils import importlib
        mod = importlib.import_module(self.module_import_name)
        return mod.__getattribute__(self.method)
        
    def process(self):
        """
        Process the dajax request calling the apropiate method.
        """
        if self.is_callable():
            #1. get the function
            thefunction = self.get_ajax_function()
            
            #2. call the function
            try:
                response = thefunction(self.request)
                if isinstance(response, Dajax):
                    return response.render()
                else:
                    return response
            except Exception, e:
                
                #Development Server Debug
                if settings.DEBUG and DajaxRequest.get_dajax_debug():
                    import traceback
                    from dajax.utils import print_green_start, print_blue_start, print_clear,print_red
                    
                    print_green_start()
                    print "#"*50
                    print "uri:      %s" % self.request.build_absolute_uri()
                    print "function: %s" % self.full_name
                    print "#"*50
                    print ""
                    print_red(str(e))
                    print_blue_start()
                    traceback.print_exc(e)
                    print_clear()
                
                # If it's an ajax request we need soft debug
                # http://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.is_ajax
                if self.request.is_ajax():
                    # If project was in debug mode, alert with Exception info
                    if settings.DEBUG:
                        response = Dajax()
                        response.alert('Exception %s: Check %s manually for more information or your server log.' %(str(e), self.request.get_full_path()))
                        return response.render()
                    # If not, check DAJAX_ERROR_CALLBACK, if present call this function
                    elif DajaxRequest.get_dajax_error_callback() != None:
                        response = Dajax()
                        response.script( DajaxRequest.get_dajax_error_callback() % str(e))
                        return response.render()
                    # Otherside ... raise Exception
                    else:
                        raise
                # If it's a non-ajax request raise Exception, Django cares.
                else:
                    raise
        else:
            raise Exception("Function not callable.")
