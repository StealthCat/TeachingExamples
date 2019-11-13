import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there_text = tk.StringVar()
        self.hi_there_text.set("Hello World")
        self.hi_there = tk.Button(self, textvariable=self.hi_there_text)
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.entry_data = tk.IntVar()
        self.entry_widget = tk.Entry(self, textvariable=self.entry_data)
        self.entry_widget.pack(side="top")

        self.enter_data = tk.Button(self, text='Submit', fg="green", 
                                    command=self.test_data)
        self.enter_data.pack(side="top")

        self.prog_bar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.prog_bar.pack(side="left")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def test_data(self):
        try:
            self.hi_there_text.set(str(self.entry_data.get()))
        except:
            self.hi_there_text.set("It's not a number")

    def say_hi(self):
        print(self.entry_data.get())

        subWindow = tk.Tk()
        app = Application(master=subWindow)
        app.mainloop()

root = tk.Tk()
app = Application(master=root)
app.mainloop()