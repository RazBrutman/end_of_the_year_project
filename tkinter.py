import Tkinter as tk
import ttk


LARGE_FONT = ("Verdana", 12)


class StreamerGui(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='favicon.ico')
        tk.Tk.wm_title(self, "Hello")

        self.geometry("350x240")
        #self.resizable(width=False, height=False)

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
        user.grid(row=0)
        self.userentry = ttk.Entry(info)
        self.userentry.grid(row=1)

        passw = ttk.Label(info, text="Password:")
        passw.grid(row=2)
        self.passwentry = ttk.Entry(info, show='*')
        self.passwentry.grid(row=3)

        info.pack(padx=10, pady=20)

        button = ttk.Button(self, text="Submit", command=lambda: self.validate(controller))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(ViewFriendInfo))
        button2.pack()


    def validate(self, cont):
        print "username:", self.userentry.get(), "password:", self.passwentry.get()
        self.userentry.delete(0, 'end')
        self.passwentry.delete(0, 'end')

        #Here should come the call to check the Database for username and password

        cont.show_frame(UserPage)


class UserPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        #label.pack(pady=10, padx=10)

        friends = VerticalScrolledFrame(self)
        friends.pack(side="right")

        label = ttk.Label(friends, text="Friends go here", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack(side="top")

        button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(ViewFriendInfo))
        button2.pack(side="top")


class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(fill="y", side="left", expand=False)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor="nw")

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


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