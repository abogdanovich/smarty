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

from django.utils import simplejson as json
from django.http import HttpResponse
from django.conf import settings

#Dajax Request
class Dajax(object):
    """
    Response methods to construct the ajax response.
    
    # Test Alert
    >>> dajax = Dajax()
    >>> dajax.alert('hello')
    >>> str(dajax.render())
    'Content-Type: text/plain\n\n[{"cmd": "alert", "val": "hello"}]'
    
    #Test assign
    >>> dajax = Dajax()
    >>> dajax.assign('#some','innerHTML','new data')
    >>> str(dajax.render())
    'Content-Type: text/plain\n\n[{"cmd": "as", "id": "#some", "val": "new data", "prop": "innerHTML"}]'
    
    """
    
    def __init__(self):
        self.calls = []
    
    """
     Tested Methods
    """
    def render(self):
        if settings.DEBUG:
            return HttpResponse(json.dumps(self.calls), mimetype="text/plain")
        return HttpResponse(json.dumps(self.calls), mimetype="application/x-json")
        
    def alert(self,message):
        self.calls.append({'cmd':'alert','val':self._clean(message)})
            
    def assign(self,id,attribute,value):
        self.calls.append({'cmd':'as','id':id,'prop':attribute,'val':self._clean(value)})
        
    def addCSSClass(self,id,value):
        if not hasattr(value,'__iter__'):
            value = [value]
        self.calls.append({'cmd':'addcc','id':id,'val':self._clean(value)})
        
    def removeCSSClass(self,id,value):
        if not hasattr(value,'__iter__'):
            value = [value]
        self.calls.append({'cmd':'remcc','id':id,'val':self._clean(value)})
    
    def append(self,id,attribute,value):
        self.calls.append({'cmd':'ap','id':id,'prop':attribute,'val':self._clean(value)})
        
    def prepend(self,id,attribute,value):
        self.calls.append({'cmd':'pp','id':id,'prop':attribute,'val':self._clean(value)})
        
    def clear(self,id,attribute):
        self.calls.append({'cmd':'clr','id':id,'prop':attribute})
        
    def redirect(self,url,delay=0):
        self.calls.append({'cmd':'red','url':url,'delay':delay})
        
    def script(self,code):#OK
        self.calls.append({'cmd':'js','val':code})
        
    def remove(self,id):
        self.calls.append({'cmd':'rm','id':id})
        
    def addData(self,data,function):
        self.calls.append({'cmd':'data','val':data,'fun':function})
    
    def _clean(self, data):
        if hasattr(data,'__iter__'):
            return map(self._clean,data)
        else:
            return str(data).replace('\n','').replace('\r','')
    
    """
     Untested Methods
    """
    
    def replace(self,id,attribute,search,replace):
        raise Exception("Not yet Implemented")
        self.calls.append({'cmd':'pp','id':id,'prop':attribute,'search':search,'replace':replace})
        
    def debug(self,message):
        raise Exception("Not yet Implemented")
        self.calls.append({'cmd':'debug','val':message})
    
    def create(self,parent,tag,id,stype):
        raise Exception("Not yet Implemented")
        self.calls.append({'cmd':'ce','parent':parent,'tag':tag,'id':id,'type':stype})
        
    def insert(self,id,before,tag):
        raise Exception("Not yet Implemented")
        self.calls.append({'cmd':'ie','id':id,'before':before,'tag':tag})
        
    def insertAfter(self,id,after,tag):
        raise Exception("Not yet Implemented")
        pass
    
    def setEvent(self,target,event,script):
        raise Exception("Not yet Implemented")
        pass
    
    def addEvent(self,target,event,script):
        raise Exception("Not yet Implemented")
        pass