# -*- coding: utf-8 -*-
import socket
import select
import os
import numpy as np
import scipy.misc as smp
from PIL import Image
import errno
import time
import msvcrt
import threading
import re

file_num = 1
reading_flag = False


def main():
    sock = socket.socket()
    sock.connect(('127.0.0.1', 54321))
    print "connected"
    request = ""
    messages = []
    while True:
        rlist, wlist, xlist = select.select([sock], [sock], [])
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == '\r':
                messages.append(request)
                request = ""
            elif char == '\x1b':
                sock.send("")
                sock.close()
                break
            else:
                request += char
                print request
        if rlist:
            data = sock.recv(1024)
            if data == "":
                sock.close()
                break
            else:
                print data

        for message in messages:
            sock.send(message)
            messages.remove(message)
    print "connection closed"
    raw_input("press any key to continue...")


if __name__ == "__main__":
    main()