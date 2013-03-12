# -*- coding: utf-8 -*-
#!/usr/bin/env python

import MySQLdb

#==========================================


def DB_INSERT(table, columns = (), values = ()):
    
    flag = False
    
    if table != '':
        try:

            conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="smarty", charset='utf8') # name of the data base
            cursor = conn.cursor()
            
            print ("INSERT INTO {0} ({1}) VALUES {2}".format(table, columns, values))
            
            cursor.execute("INSERT INTO {0} ({1}) VALUES {2}".format(table, columns, values))
            conn.commit()
            flag = True
    
        except IOError, e:
            #TODO: log db error instead of print
            print "Error %d: %s" % (e.args[0],e.args[1])
            
        finally:
            if cursor:
                cursor.close()
            
            if conn:
                conn.close()
    
    else:
        #TODO: log db error instead of print
        print 'table name is empty'
        
    return flag


def DB_SELECT(table, condition = ''):
    
    numrows = 0
    results = []
    
    if table != '':
        try:
    
            conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="smarty", charset='utf8') # name of the data base
            cursor = conn.cursor()
            
            if condition != '':
            
                print ("SELECT * FROM {0} WHERE {1}" .format(table, condition))
                
                cursor.execute("SELECT * FROM {0} WHERE {1}" .format(table, condition))
            else:
                
                cursor.execute("SELECT * FROM {0}".format(table))
            
            #get selected row count
            numrows = int(cursor.rowcount)
            
            #fetch table records
            results = cursor.fetchall()
    
        except IOError, e:
            #TODO: log db error instead of print
            print "Error %d: %s" % (e.args[0],e.args[1])
            
        finally:
            if cursor:
                cursor.close()
            
            if conn:
                conn.close()
    
    else:
        print 'need to select db table name!'
        
    return numrows, results

#==========================================

def DB_UPDATE(table, columns, condition):
    
    flag = False
    #SID = db address field instead of id table record
    
    if table != '' and columns != '' and condition != '':
        try:

            conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="smarty", charset='utf8') # name of the data base
            cursor = conn.cursor()
            
            print ("UPDATE {0} SET {1} WHERE {2}".format(table, columns, condition))
            
            cursor.execute("UPDATE {0} SET {1} WHERE {2}".format(table, columns, condition))
            conn.commit()
            flag = True

        except IOError, e:
            #TODO: log db error instead of print
            print "Error %d: %s" % (e.args[0],e.args[1])
            
        finally:
            if cursor:
                cursor.close()
            
            if conn:
                conn.close()
    
    else:
        #TODO: log db error instead of print
        print 'table\columns or condition are empty'
        
    return flag

#==========================================
    
#get all sensors

print 'show 28 sensors'
slist = DB_SELECT('web_sensor', 'family=28')

for row in slist[1] :
        print row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        
print "----"

print 'show all sensors'
slist = DB_SELECT('web_sensor')


for row in slist[1] :
        print row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        
print "----"

if (DB_UPDATE('web_sensor', "alias='ПОЛНАЯ_ЖОПА'", "id='9'")):
    print "update is OK"
else:
    print "fail to update!"

print "----"


if (DB_INSERT('web_sensordata', ('sensor, data, date'), ('9','1','111111'))):
    print "INSERT is OK"
else:
    print "fail to INSERT!"

