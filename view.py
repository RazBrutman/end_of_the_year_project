import Tkinter as tk
import ttk


LARGE_FONT = ("Verdana Bold", 24)
SMALL_FONT = ("Times New Roman", 12)


class StreamerGui(object):

    def __init__(self, master):

        window = tk.Frame(master)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}

        """for F in (StartPage, UserPage, ViewFriendInfo):

            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame = StartPage(window)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()"""

        self.frame = StartPage(window)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()



class StartPage(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)


        label = ttk.Label(self, text="Welcome to Streamer!", font=LARGE_FONT)
        label.pack(pady=50)
        info = tk.Frame(self)
        user = ttk.Label(info, text="Username:", font=SMALL_FONT)
        user.grid(row=0)
        self.userentry = ttk.Entry(info)
        self.userentry.grid(row=1, column=0, columnspan=2)
        passw = ttk.Label(info, text="Password:", font=SMALL_FONT)
        passw.grid(row=2)
        self.passwentry = ttk.Entry(info, show='*')
        self.passwentry.grid(row=3)
        info.pack(padx=10, pady=20)
        self.sub = ttk.Button(self, text="Submit", command=lambda: self.validate())
        self.sub.pack()

        #button2 = ttk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(ViewFriendInfo))
        #button2.pack()

    def validate(self):
        self.userentry.delete(0, 'end')
        self.passwentry.delete(0, 'end')

        #Here should come the call to check the Database for username and password
        #cont.show_frame(UserPage)


