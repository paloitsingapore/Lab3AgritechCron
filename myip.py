#!/usr/bin/python3
import socket
import os
import time
 
def GetIP():
    for x in range (20):
        try:
            gw = os.popen("ip -4 route show default").read().split()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((gw[2], 0))
            ipaddr = s.getsockname()[0]
            return ipaddr
        except:
            print('Router is not connected. No IP Yet!!!')
            time.sleep(30)
