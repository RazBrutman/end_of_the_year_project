# -*- coding: utf-8 -*-
import socket
import select
import msvcrt
import os
#import gui


class Client(object):

    def __init__(self, SERVER_IP, PORT):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((SERVER_IP, PORT))
            print "connected"
            self.sock_object = sock
        except socket.error:
            print "Server not found!"

    def send_msg(self, msg, **kwargs):

        if 'type' in kwargs:
            print kwargs['type']

        if self.sock_object:
            self.sock_object.send(msg)

    def recv_msg(self):

        if self.sock_object:
            return self.sock_object.recv(1024)




def main():

    file_num = 1
    reading_flag = False
    process_file_packets = []

    SERVER_IP = '127.0.0.1'
    connected = False

    #Connecting to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, 54321))
        connected = True
        print "connected"
    except socket.error:
        print "Server not found!"

    request = ""
    messages = []
    while connected:
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
                    if "!!END!!" in data:
                        reading_flag = False
                        if data != "!!END!!":
                            process_file_packets.append(data[data.find("!!END!!") + 7:])
                        process_file_packets, file_num = reassemble_file(process_file_packets, file_num)
                    else:
                        process_file_packets.append(data)
                elif "!!START!!" in data:
                    reading_flag = True
                    if data != "!!START!!":
                        process_file_packets.append(data[data.find("!!START!!") + 9:])
                else:
                    print data
        for message in messages:
            sock.send(message)
            messages.remove(message)
    print "connection closed"
    #raw_input("press any key to continue...")




def reassemble_file(pfp, file_num):
    file_name = "file_{}.jpg".format(file_num)
    while file_name in os.listdir(os.getcwd()):
        file_num += 1
        file_name = "file_{}.jpg".format(file_num)
    f = open(file_name, "ab")
    for item in pfp:
        f.write(item)
    f.close()
    return [], file_num


