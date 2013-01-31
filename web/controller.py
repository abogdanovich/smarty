# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system controllers
# author Alex Bogdanovich
# 2013 
#########################################################################

#########################################################################
#Controller class 
#########################################################################

class Controller:
    def __init__(self, uid, alias, type, status):
        self.uid = uid
        self.alias = alias
        self.type = type
        self.status = status
        return self.uid

