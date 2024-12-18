#this is a clock app
#appinventor name by phone:"mati clock appinventor"
#there will be 4 buttons
import datetime

import tkinter as tk

class ClockApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        tk.Button(self, text="óra léptetés", command=self.ora_leptetes).grid(column=0, row=0)
        tk.Button(self, text="idő léptetés", command=self.ido_leptetes).grid(column=1, row=0)
        tk.Button(self, text="óra le").grid(column=0, row=4)
        tk.Button(self, text="idő le").grid(column=1, row=4)

        self.time = tk.Label(self, text="00:00", font=("Arial", 48))
        self.time.grid(column=0, row=2)

    def ora_leptetes(self):
        self.set_time(hour=1, minute=0)
    
    def ido_leptetes(self):
        self.set_time(hour=0, minute=1)

    def set_time(self, hour=0, minute=0):
        timeobj = datetime.datetime.strptime(self.time['text'], "%H:%M")
        timeobj += datetime.timedelta(hours=hour, minutes=minute)
        self.time.config(text=datetime.datetime.strftime(timeobj, "%H:%M"))

root = tk.Tk()
myapp = ClockApp(root)
root.title = 'mati clock appinventor'
root.attributes("-fullscreen", True)
myapp.mainloop()
