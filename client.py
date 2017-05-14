# -*- coding: utf-8 -*-
import socket
import select
import sys
import os
import numpy as np
import scipy.misc as smp
from PIL import Image
import errno
import time
import msvcrt
import threading
import re


def main():

    file_num = 1
    reading_flag = False
    proccess_file_packects = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 54321))
    print "connected"
    request = ""
    messages = []
    while True:
        rlist, wlist, xlist = select.select([sock], [sock], [])
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == '\r':
                print
                messages.append(request)
                request = ""
            elif char == '\x1b':
                sock.close()
                break
            else:
                if char == "\x08":
                    request = request[:-1]
                    print request, ' \b\r',
                else:
                    request += char
                    print request + '\r',
        if rlist:
            data = sock.recv(1024)
            if data == "":
                break
            else: #there is data to be read
                if reading_flag:
                    proccess_file_packects.append(data)
                    if "!!END!!" in data:
                        reading_flag = False
                        proccess_file_packects, file_num = reassemble_file(proccess_file_packects, file_num)
                elif "!!START!!" in data:
                    reading_flag = True
                    proccess_file_packects.append(data)
                else:
                    print data
        for message in messages:
            sock.send(message)
            messages.remove(message)
    print "connection closed"
    raw_input("press any key to continue...")


def reassemble_file(pfp, file_num):
    f = open("file_{}.jpg".format(file_num), "ab")
    file_num += 1
    pfp.remove("!!START!!")
    pfp.remove("!!END!!")
    for item in pfp:
        f.write(item)
    f.close()
    return [], file_num


if __name__ == "__main__":
    main()
