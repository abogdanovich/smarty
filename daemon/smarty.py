# -*- coding: utf-8 -*-
#!/usr/bin/env python

import subprocess, os, pynotify, logging, tempfile, ConfigParser, sys
from datetime import datetime
import ow

class Smarty:
    useNotifySend       = True
    useNotifySound      = False #no yet
    daemonTimeout       = 0.5 #sec
    testvar             = 1

    def __init__(self):
        # log init
        logging.basicConfig(filename = tempfile.gettempdir() + '/smarty.log',
                            level = logging.DEBUG,
                            format = '%(asctime)s %(levelname)s: %(message)s',
                            datefmt = '%Y-%m-%d %I:%M:%S')
        logging.info('Daemon start')
        
        #ow init

        # start notify
        #self.fireNotify('Start!')

    def fireNotify(self, msg = '', title = 'Smarty Home System'):
        """
        Fire notify action
        """
        logging.info('Called fireNotify()')
        
        if (self.useNotifySend):
        
            #commands.getstatusoutput('notify-send -u "%s" -i "%s" "%s" "%s"' % (level, icon, title, msg))
            if pynotify.init('icon-summary-body'):
               
                pynotify.Notification(title, msg, self.getSystemIcon()).show()
            else:
                
                print 'Notify not supported. You need to install python-notify package first.'

        if (self.useNotifySound):
            # play sound event
            #if (self.useNotifySound):
            pass

    def getSystemIcon(self):
        """
        Get system icon path
        example: notification-power-disconnected
        """
        return ''

    def getLastCheckTime(self):
        """
        To simplicity, time of last modification of the current file is used as the time of last checking
        """
        lastCheckTime = os.path.getmtime(__file__)
        return datetime.fromtimestamp(lastCheckTime)

    def setLastCheckTime(self, time = None):
        """
        Set time of last checking -> touch file
        """
        #commands.getoutput('touch ' + __file__)
        #os.system('touch ' + __file__)
        subprocess.check_output('touch ' + __file__, shell=True)
        return self

    def getRepositoryPath(self):
        """
        Get repository path
        """
        return self.repositoryPath

    def getDaemonTimeout(self):
        """
        Get daemon checking timeout
        """
        return self.daemonTimeout

    def check(self, lastCheckTime = None, repositoryPath = None):
        """
        Get git log as string
        """
        logging.info('Called check()')
        #if (not lastCheckTime):
        #    lastCheckTime = self.getLastCheckTime()

        
        #only for test
        self.testvar += 1
        logging.info('testvar: %s', self.testvar)
        """

        if (countCommits > 0):
            logging.info('Test new changes: %s', countCommits)
            message += '...\n%s new commit(s)\n\n' % countCommits

            #self.fireNotify(message)
            #self.setLastCheckTime()
        """
        logging.info('End check()')
        return self

if __name__ == '__main__':
    c = Smarty()
    c.check()