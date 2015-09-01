# -*- coding: cp936 -*-
import sys
import time
from socket import socket, SOCK_DGRAM, AF_INET

from myproject.cplustools import Msg_Sender

try:
    import psutil
except ImportError:
    print 'please install psutil module. for example :' \
          'pip install psutil'
    sys.exit(1)



def sendmsg(phone,msg):
    msg_send_code = Msg_Sender.Msg_rpc().send_phone_msg(phone,msg)
    return msg_send_code

class SystemInfo(object):

    def cpu_stat(self):
        interval=1
        cpu_useage = psutil.cpu_percent(interval)
        return cpu_useage

    def memory_stat(self):
        mem = {}
        f = open("/proc/meminfo")
        lines = f.readlines()
        f.close()
        for line in lines:
            if len(line) < 2: continue
            name = line.split(':')[0]
            var = line.split(':')[1].split()[0]
            mem[name] = long(var) * 1024.0
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
        return mem

    def disk_stat(self):
        import os
        hd={}
        disk = os.statvfs("/home")
        hd['available'] = (disk.f_bsize * disk.f_bavail) /1024
        hd['capacity'] = (disk.f_bsize * disk.f_blocks) / 1024
        hd['used'] = (disk.f_bsize * (disk.f_blocks - disk.f_bfree)) /1024
        return hd

class Monitor(SystemInfo):
    def __init__(self):
        self.cpu_threshold = 70
        self.mem_threshold = 70
        self.hd_threshold = 70
        self.msg = ''
        s = socket(AF_INET, SOCK_DGRAM)
        s1 = socket(AF_INET, SOCK_DGRAM)
        s.connect(('192.168.0.1', 0))
        s1.connect(('114.114.114.114', 0))
        self.local_ip = s.getsockname()[0]
        self.int_ip = s1.getsockname()[0]

    def system_stat(self):
        cpu_useage = self.cpu_stat()
        if cpu_useage > self.cpu_threshold :
            self.msg +=  'Warning: Host %s cpu used over %.2f%% !\n' % (self.int_ip,cpu_useage)

        meminfo =  self.memory_stat()
        mem_used = meminfo['MemUsed']
        mem_total = meminfo['MemTotal']
        percent_memuseage = (float(mem_used) / float(mem_total)) * 100
        if percent_memuseage >  self.mem_threshold:
            self.msg +=  'Warning: Host %s mem used over %.2f%% !\n' % (self.int_ip,percent_memuseage)

        hdinfo = self.disk_stat()
        hd_used = hdinfo['used']
        hd_total= hdinfo['capacity']
        percent_hduseage = (float(hd_used) / float(hd_total)) * 100
        if percent_hduseage >  self.hd_threshold:
            self.msg +=  'Warning: Host %s disk space used over %.2f%% !\n' % (self.int_ip,percent_hduseage)

        if self.msg :
            return self.msg
        return


if __name__ == '__main__':
    # phone_list = ['18086669830','15207125813']
    phone_list = ['15207125813','15002751813']
    warning_count = 0
    while 1:
        stats_msg = Monitor().system_stat()
        if stats_msg:
            warning_count += 1
            if warning_count <= 2:
                sleep_second = 600
            if  warning_count > 2 and warning_count <= 6:
                sleep_second = 1800
            if  warning_count > 6 and warning_count < 10:
                sleep_second = 3600
            if warning_count >= 10 :
                sleep_second = 10800
                warning_count = 0
            for phone in phone_list:
                # print stats_msg
                print sendmsg(phone,stats_msg)
                time.sleep(1)
            time.sleep(sleep_second)
# sendmsg('18086669830','1321test')
