from datetime import datetime
from myproject.cplustools.component_controler import *
from PyServerMonitor import *


def deamon(MsgRepeaters):
    for MsgRepeater in MsgRepeaters:
        component = Action(MsgRepeater)
        if not component.isalived():
            component.start()
            content = '%s was down, now get starting.' % MsgRepeater
            writelog(content)

def stopMsgRepeater(MsgRepeaters):
    for MsgRepeater in MsgRepeaters:
        component = Action(MsgRepeater)
        component.stop()
        content = '%s was shutdown by deamon process.' % MsgRepeater
        writelog(content)


def checkmemused():
     meminfo =  SystemInfo().memory_stat()
     mem_used = meminfo['MemUsed']
     mem_total = meminfo['MemTotal']
     percent_memuseage = (float(mem_used) / float(mem_total)) * 100
     if int(percent_memuseage) >  97:
         content = 'memory used over %.2f%% !\n' % percent_memuseage
         writelog(content)
         return True
     return False


def writelog(content, logfile = 'Process_deamon.log'):
    f = open(logfile,'a')
    f.write('%s %s\n' % (datetime.now(),content))
    f.close()


if __name__ == '__main__':
    MsgRepeaters = ['MsgRepeater1','MsgRepeater2','MsgRepeater3','MsgRepeater4']
    while 1:
        if checkmemused():
            stopMsgRepeater(MsgRepeaters)
        deamon(MsgRepeaters)
        time.sleep(10)