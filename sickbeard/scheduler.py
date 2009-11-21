import datetime
import time
import threading
import traceback

from sickbeard.logging import *

class Scheduler:

    def __init__(self, action, cycleTime=datetime.timedelta(minutes=10), runImmediately=True, threadName="ScheduledThread", silent=False):

        if runImmediately:
            self.lastRun = datetime.datetime.fromordinal(1)
        else:
            self.lastRun = datetime.datetime.now()

        self.action = action
        self.cycleTime = cycleTime
        
        self.thread = None
        self.threadName = threadName
        self.silent = silent
        
        self.initThread()
        
        self.abort = False
    
    def initThread(self):
        if self.thread == None or not self.thread.isAlive():
            self.thread = threading.Thread(None, self.runAction, self.threadName)
    
    def runAction(self):
        
        while True:
            
            currentTime = datetime.datetime.now()
            
            if currentTime - self.lastRun > self.cycleTime:
                self.lastRun = currentTime
                try:
                    if not self.silent:
                        Logger().log("Starting new thread: "+self.threadName, DEBUG)
                    self.action.run()
                except Exception as e:
                    Logger().log("Exception generated in thread "+self.threadName+": " + str(e), ERROR)
                    Logger().log(traceback.format_exc(), DEBUG)
            
            if self.abort:
                self.abort = False
                self.thread = None
                return
            
            time.sleep(1) 