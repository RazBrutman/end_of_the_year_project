import Tkinter as tk
import ttk


LARGE_FONT = ("Verdana", 12)


class StreamerGui(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='favicon.ico')
        tk.Tk.wm_title(self, "Hello")

        self.geometry("350x220")
        self.resizable(width=False, height=False)

        #self.attributes("-alpha", 0.7)
        #self.wm_attributes("-transparentcolor", "yellow")

        window = tk.Frame(self)
        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, UserPage, ViewFriendInfo):

            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Tk.title(controller, "")


        label = ttk.Label(self, text="Welcome to Streamer!", font=LARGE_FONT)
        label.pack(pady=10)

        info = tk.Frame(self)

        user = ttk.Label(info, text="Username:")
        user.grid(row=0, column=0)
        self.userEntry = ttk.Entry(info)
        self.userEntry.grid(row=0, column=1)

        passw = ttk.Label(info, text="Password:")
        passw.grid(row=1, column=0)
        self.passwEntry = ttk.Entry(info, show='*')
        self.passwEntry.grid(row=1, column=1)

        info.pack(padx=10, pady=30)

        button = ttk.Button(self, text="Submit", command=lambda: self.validate(controller))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(ViewFriendInfo))
        button2.pack()


    def validate(self, cont):
        print "username:", self.userEntry.get(), "password:", self.passwEntry.get()
        #self.userEntry.delete(0, 'end')
        #self.passwEntry.delete(0, 'end')
        cont.show_frame(UserPage)


class UserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(ViewFriendInfo))
        button2.pack()


class ViewFriendInfo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(UserPage))
        button2.pack()
        

app = StreamerGui()
app.mainloop()