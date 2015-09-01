#coding: utf-8
import sys
import getpass
import os
import time
import re
import subprocess


try:
    from screenutils import list_screens, Screen
except ImportError:
    print 'please install screenutils module. for example :' \
          'pip install screenutils'
    sys.exit(1)

try:
    import psutil
except ImportError:
    print 'please install psutil module. for example :' \
          'pip install psutil'
    sys.exit(1)



class Component_base(object):

    def __init__(self,component_name):
        self.rooms_path = '/home/room/server'
        self.component_name = component_name

    #判断screen是否存在
    def get_screens(self):
        for screen in list_screens():
            if self.component_name.lower() in screen.name.lower():
                return screen
        return

    #创建新的screen
    def NewScreen(self):
        self.screen = Screen(self.component_name,True)
        return self.screen

    #获取组件所在路径
    def getpwd(self):
        allroom = os.listdir(self.rooms_path)
        for room in allroom:
            if room.lower() == self.component_name.lower():
                self.room_path = os.path.join(self.rooms_path,room)
                return  self.room_path   #'/home/room/server/ChatRoom31'
        return

    #进程是否存活
    def isalived(self):
        ps = psutil.process_iter()
        for self.psinfo in ps:
            try:
                if self.component_name.lower() == self.psinfo.name().lower():
                    return self.psinfo
            except:
                continue
        return

class Action(Component_base):

    def __init__(self,component_name):
        Component_base.__init__(self,component_name)
        self.screen = self.get_screens()

    def start(self):
        if not self.isalived():
            if not self.get_screens():
                self.NewScreen()
            path = self.getpwd()
            self.screen.send_commands('cd '+  path)
            self.screen.send_commands('./'+self.component_name)
            result =  '%s started success!' % self.component_name
            print result
            return result
        else:
            result =  '%s is already running !' % self.component_name
            print  result
            return result

    def stop(self):
        if self.isalived():
             self.component_process = self.isalived()
             self.component_process.kill()
             result = '%s stopped success' % self.component_name
             print  result
             return result
        else:
             result = '%s was not started' % self.component_name
             print  result
             return result

    def sendcmd(self,segment):
        if self.isalived():
            #screen = self.get_screens()
            self.screen.send_commands(segment)
            result = 'send command to %s success!' % self.component_name
            print result
            return result




if __name__ == '__main__':
    components_name = sys.argv[1]
    segment = sys.argv[2]
    if len(sys.argv) < 3:
        print 'segment error! '
        sys.exit(1)
    else:
        try :
            components_list = eval(components_name)
        except :
            print "%s is illegal components_name" % components_name
            sys.exit(1)

    for components_name in components_list:
        component = Action(components_name)
        if segment == 'start':
            component.start()
        elif segment == 'stop':
            component.stop()
        elif  segment == 'restart':
            component.stop()
            time.sleep(0.5)
            component.start()
        elif segment == 'checkhideroom':
            component.checkhideroom()
        else:
            component.sendcmd(segment)



