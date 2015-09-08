# coding: utf-8
from socket import socket, SOCK_DGRAM, AF_INET
import MySQLdb
from datetime import datetime
from component_controler import *



def writelog(content, logfile = 'Process_deamon.log'):
    f = open(logfile,'a')
    f.write('%s %s\n' % (datetime.now(),content))
    f.close()

class ComponentStatus(object):
    def __init__(self):
        """

            get components infomation from database
        """
        self.rooms_path = '/home/room/server'
        s = socket(AF_INET, SOCK_DGRAM)
        s1 = socket(AF_INET, SOCK_DGRAM)
        s.connect(('192.168.4.1', 0))
        s1.connect(('114.114.114.114', 0))
        self.local_ip = s.getsockname()[0]
        self.int_ip = s1.getsockname()[0]

        self.conn=MySQLdb.connect(user='username',passwd='password',host='192.168.4.11', port=3306)
        self.cursor_components = self.conn.cursor()
        self.cursor_msgserver = self.conn.cursor()
        self.cursor_components.execute("use stt_config")
        self.cursor_components.execute('select server_name,ip from web_server_info where ip = "%s"' % self.int_ip)
        self.cursor_msgserver.execute("use stt_config")
        self.cursor_msgserver.execute('select server_id from msg_server_info where ip="%s"' % self.local_ip)
        self.components = {}
        self.msgserver = []
        for servername,ip in self.cursor_components.fetchall():
            self.components[servername] = ip
        for server_id in self.cursor_msgserver.fetchall():
            self.msgserver.append(int(server_id[0]))
        self.cursor_components.close()
        self.conn.close()

    def deamon(self,debug=False):
        for component_name in self.components:
            component = Action(component_name)
            if debug:
                print component_name
                continue
            if not component.isalived():
                content = '%s was shutdown.' % component_name
                writelog(content)
                component.start()
                content = '%s was down, now get starting.' % component_name
                writelog(content)

        for msgserver_num in self.msgserver:
            msgserver_name = 'MsgServer' + str(msgserver_num)
            component = Action(msgserver_name)
            if debug:
                print msgserver_name
                continue
            if not component.isalived():
                content = '%s was shutdown.' % msgserver_name
                writelog(content)
                component.start()
                content = '%s was down, now get starting.' % msgserver_name
                writelog(content)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'debug':
            ProcessDaemon = ComponentStatus()
            ProcessDaemon.deamon(debug=True)
            sys.exit()
        else:
            print 'Illegal Segment! Now Exit...'

    while 1:
        try:
            ProcessDaemon = ComponentStatus()
        except:
            sys.exit(1)
        ProcessDaemon.deamon()
        time.sleep(10)
