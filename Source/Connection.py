from pycomm3 import LogixDriver, SLCDriver
from tkinter import *
from PIL import ImageTk
from CIP import *
import re
from future.moves.tkinter import messagebox

class First_Access(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_user_interface()
    def connection(self):
        valid = re.compile(r'((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))((^|\.)((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]?\d))){3}$')  #IP pattern
        if valid.search(self.ip.get()):
            try:
                with LogixDriver(self.ip.get()) as plc:
                    ip = self.ip.get()
                    messagebox.showinfo("IP : " + self.ip.get(), "Connected with LogixDrivers")
                    window.destroy()
                    newindow = Tk()
                    application = mainapp(newindow, plc, ip)
                    newindow.mainloop()
            except:
                try:
                    with SLCDriver(self.ip.get()) as plc:
                        messagebox.showinfo("IP : " + self.ip.get(), "Connected with SLCDriver")        #For Plcs that can open with Logic Studio 500
                        window.destroy()
                        newindow = Tk()
                        application = mainapp(newindow, plc)
                        newindow.mainloop()
                except:
                    pass
                messagebox.showerror("IP : " + self.ip.get(), "Connection refused, Failed to open a connection")
        else: messagebox.showwarning("IP : " + self.ip.get(), "Please enter a valid IP")
        
    def initialize_user_interface(self):
        self.parent.title("PLCs Login")
        self.parent.geometry("500x300")
        self.parent.resizable(False, False)

        self.bg = ImageTk.PhotoImage(file = "bg.jpg")
        self.bg_image = Label(self.parent, image = self.bg).place(x = 0, y = 0, relwidth = 1,relheight = 1)
        
        self.IPframe = LabelFrame(self.parent, text = "Enter IP", font = ("Impact", 20, "bold")).place(x = 100, y = 100, height = 150, width = 300)

        data = StringVar
        self.ip = Entry(self.IPframe, textvariable = data, font = ("Times new roman", 15), bg = "lightgray")
        self.ip.place(x = 150, y = 150)

        self.btn = Button(self.IPframe, command = self.connection, text = "Valid IP", font = 'Times 15').place(x = 205, y = 200)

if __name__ == "__main__":
    window = Tk()
    app = First_Access(window)
    app.mainloop()

