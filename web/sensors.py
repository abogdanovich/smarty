# -*- coding: utf-8 -*-

#########################################################################
# Smarty home system sensors
# author Alex Bogdanovich
# 2013 
#########################################################################

#########################################################################
#Sensors classes
#########################################################################

class Sensor:
    def __init__(self, uid, alias, type, status, value, date, access_time):
        self.uid = uid
        self.alias = alias
        self.type = type
        self.status = status
        self.value = value
        self.access_time = access_time
        return self.uid

