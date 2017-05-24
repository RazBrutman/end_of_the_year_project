# -*- coding: utf-8 -*-
import socket
import select
import msvcrt
import os

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



