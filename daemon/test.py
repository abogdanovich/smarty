# -*- coding: utf-8 -*-
#!/usr/bin/env python

import MySQLdb

#==========================================

def DB_SELECT(TABLE, PARAM = '', SIGN = '', VALUE = ''):
    
    numrows = 0
    records = []
    
    if TABLE != '':
        try:
    
            conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="smarty", charset='utf8') # name of the data base
            cursor = conn.cursor()
            
            if PARAM != '' and SIGN != '' and VALUE != '':
            
                cursor.execute("SELECT * FROM %s WHERE %s %s %s" % (TABLE, PARAM, SIGN, VALUE))
            else:
                
                cursor.execute("SELECT * FROM %s" % (TABLE))
            
            #get selected row count
            numrows = int(cursor.rowcount)
            
            #fetch table records
            records = cursor.fetchall()
    
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
        
    return numrows, records

#==========================================

def DB_UPDATE(TABLE, PARAM = '', VALUE = '', SID = ''):
    
    flag = False
    #SID = db address field instead of id table record
    
    if TABLE != '':
        try:

            conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="smarty", charset='utf8') # name of the data base
            cursor = conn.cursor()
            
            if PARAM != '' and VALUE != '' and SID != '':
                cursor.execute("UPDATE %s SET %s='%s' WHERE address='%s'" % (TABLE, PARAM, VALUE, SID))
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
        print 'TABLE name is empty'
        
    return flag

#==========================================
    
#get all sensors

print 'show all sensors'
slist = DB_SELECT('web_sensor')
print 'all sensors > %s row count' % slist[0]
for row in slist[1] :
        print row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]

print 'update sensor'

if (DB_UPDATE('web_sensor', 'alias', 'ГОСТЕВАЯ', '1111')):
    print "update is OK"
else:
    print "fail to update!"

slist = DB_SELECT('web_sensor')
for row in slist[1] :
        print row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        

