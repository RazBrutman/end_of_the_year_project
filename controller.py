# -*- coding: utf-8 -*-
from model import Client
from view import StreamerGui
import Tkinter as tk


class Controller(object):

    def __init__(self, ip, port):
        self.root = tk.Tk()
        self.model = Client(ip, port)
        self.view = StreamerGui(self.root)

    def run(self):
        root = self.root
        self.view.frame.sub.bind("<Button>", self.validate)
        root.geometry("500x380")
        root.resizable(width=False, height=False)
        root.iconbitmap(r'c:\\end_of_the_year_project-master\\favicon.ico')
        root.title("fuck you")
        root.deiconify()
        root.mainloop()


    def validate(self, event):
        un = self.view.frame.userentry.get()
        pw = self.view.frame.passwentry.get()
        print un, pw

