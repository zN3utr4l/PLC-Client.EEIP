from pycomm3 import LogixDriver, SLCDriver
from tkinter import *
import tk_tools
import re
from future.moves.tkinter import messagebox
import datetime
import time
from PIL import ImageTk
from tkinter.ttk import Combobox
from time import sleep
from DataType import *

i = 1

class mainapp:
    def __init__(self, parent, plc, ip):
        self.parent = parent
        self.plc = plc
        self.ip = ip
        self.initialize_user_interface_main()
        
    def initialize_user_interface_main(self):
        self.parent.title('PLCs Option')
        self.parent.geometry("700x700")
        self.parent.resizable(False, False)
        
        self.bg = ImageTk.PhotoImage(file = "logo.png")
        self.bg_image = Label(self.parent, image = self.bg).place(x = 0, y = 0, relwidth = 1,relheight = 1)

        self.lblInfo = Label(self.parent, font=('arial', 20, 'bold'), anchor = 's', fg='Dark green')
        self.lblInfo.place(x = 95, y = 660)
        self.tick()

        self.led = tk_tools.Led(self.parent, size=50, on_click_callback = self.click, toggle_on_click = True)
        self.led.to_green(True)
        self.led.place(x = 640, y = -5)

        #self.btn = Button(self.parent, command = self.get_data_types, text = "Print all Tags", font = 'Times 15').place(x = 0, y = 0)

        self.Infoframe = LabelFrame(self.parent, text = "Info", font = ("Impact", 20, "bold")).place(x = 330, y = 50, height = 200, width = 350)

        self.vendor = Label(self.Infoframe, font = 'Helvetica 12', text = ("Vendor: " + self.plc.info['vendor']), bg = "lightgray").place(x = 340, y = 90)
        self.product_type = Label(self.Infoframe, font = 'Helvetica 12', text = ("Product type: " + self.plc.info['product_type']), bg = "lightgray").place(x = 340, y = 120)
        self.product_code = Label(self.Infoframe, font = 'Helvetica 12', text = ("Product code: " + str(self.plc.info['product_code'])), bg = "lightgray").place(x = 340, y = 150)
        self.device_type = Label(self.Infoframe, font = 'Helvetica 12', text = ("Device type: " + self.plc.info['device_type']), bg = "lightgray").place(x = 340, y = 180)
        self.serial = Label(self.Infoframe, font = 'Helvetica 12', text = ("Serial: " + self.plc.info['serial']), bg = "lightgray").place(x = 340, y = 210)

        self.Tagframe = LabelFrame(self.parent, text = "Read a specific Tag", font = ("Impact", 20, "bold")).place(x = 10, y = 50, height = 150, width = 300)

        self.cmb = Combobox(self.Tagframe, width = 10)
        self.cmb.place(x = 20, y = 110, width = 280)

        self.num_tag = IntVar()
        self.lblTag = Label(self.Tagframe, font = 'Helvetica 15', textvariable = self.num_tag).place(x = 265, y = 70)
        self.btn_select = Button(self.Tagframe, command = self.select_tag , text = "Select Tag", font = 'Times 15').place(x = 20, y = 150)
        self.btn_select = Button(self.Tagframe, command = self.load_tag , text = "Load Tags", font = 'Times 15').place(x = 200, y = 150)

        self.Readframe = LabelFrame(self.parent, text = "Read View", font = ("Impact", 20, "bold")).place(x = 10, y = 400, height = 150, width = 300)

        self.tag_name = StringVar()
        self.tag_value = StringVar()
        self.tag_value_new = StringVar()
        self.tag_type = StringVar()
        self.name_read = Label(self.Readframe, font = 'Helvetica 12', textvariable = self.tag_name, bg = "lightgray").place(x = 20, y = 440)
        self.value_read = Label(self.Readframe, font = 'Helvetica 12', textvariable = self.tag_value, bg = "lightgray").place(x = 20, y = 470)
        self.data_type_read = Label(self.Readframe, font = 'Helvetica 12', textvariable = self.tag_type, bg = "lightgray").place(x = 20, y = 500)

        self.Writeframe = LabelFrame(self.parent, text = "Write View", font = ("Impact", 20, "bold")).place(x = 330, y = 400, height = 170, width = 350)

        self.name_write = Label(self.Writeframe, font = 'Helvetica 12', textvariable = self.tag_name, bg = "lightgray").place(x = 350, y = 440)
        self.value_lbl = Label(self.Writeframe, font = 'Helvetica 12', text = 'Value: ', bg = "lightgray").place(x = 350, y = 470)
        self.value_write = Entry(self.Writeframe, font = 'Helvetica 12', textvariable = self.tag_value_new, bg = "lightgray")
        self.value_write.place(x = 410, y = 470)
        self.data_type_write = Label(self.Writeframe, font = 'Helvetica 12', textvariable = self.tag_type, bg = "lightgray").place(x = 350, y = 500)
        self.btn_write = Button(self.Writeframe, command = self.write_tag, text = "Update Tag", font = 'Times 15').place(x = 560, y = 520)


    def tick(self):
        d = datetime.datetime.now()
        today = '{:%B %d,%Y}'.format(d)

        mytime = time.strftime('%I:%M:%S%p')
        self.lblInfo.config(text=(mytime + '\t' + today))
        self.lblInfo.after(200, self.tick)

    """
    def get_data_types(self):
        for typ in self.plc.data_types:
            print(f'{typ} attributes: ', self.plc.data_types[typ]['attributes'])
        tag_count = len(self.plc.tags)
        print(f'There are {tag_count} tags')
    """

    def select_tag(self):
        if(self.cmb.get()):
            """
            if((self.plc.tags[self.cmb.get()])['dimensions'] and (self.plc.tags[self.cmb.get()])['dimensions'][0]) >= 1:                #FIRST IDEA TO MANAGE ARRAY
                self.plcTag = self.plc.read(self.cmb.get() + '{' + str((self.plc.tags[self.cmb.get()])['dimensions'][0]) + '}')         #IMPLEMENTATION IN load_tag
                #print(self.plcTag)
                self.tag_name.set('Tag name: ' + self.plcTag.tag)             #His name
                self.tag_value.set(("Value: " + str(self.plcTag.value)))        #His Value
                self.tag_value_new.set(("Value: " + str(self.plcTag.value)))    #My new Value
                self.tag_type.set(("Data Type: " + self.plcTag.type))           #His type
            else:
            """ 
            self.plcTag = self.plc.read(self.cmb.get())
            self.tag_name.set(("Tag name: " + self.plcTag.tag))             #His name
            #print(self.plcTag.value[3])
            self.tag_value.set(("Value: " + str(self.plcTag.value)))        #His Value
            self.tag_value_new.set(str(self.plcTag.value))                  #My new Value
            self.tag_type.set(("Data Type: " + str(self.plcTag.type)))      #His type
        else: messagebox.showwarning("IP : " + self.ip, "Select a valid Tag")

    def write_tag(self):
        error = 0
        if(self.tag_value_new.get()):
            #print(type(self.tag_value_new.get()), self.tag_value_new.get())
            value = self.tag_value_new.get()                                                          # IF ['tag_type'] == 'struct' ERROR: ValueError: too many values to unpack (expected 2)
            #x, value = x.split(":")                                                                 # Split 'Value: ' from value
            #value = str(value).strip("[ ]")                                                         # and convert all in class 'list'
            #value = value.split(", ")                                                               # E.g. self.plcTag {Tag : Login, Value : True, Type : bool}
            #print(type(value))                                                                      #       <class 'list'>
            #print(value)                                                                            #       value = ['True']
            #print(type(value[0]))                                                                   #       <class 'str'>
            try:
                data_type = self.get_tag_datatype()
                convert_func = TypeFunctionMap[data_type]
                if(convert_func == bool):
                    if(self.elements > 1):
                        new_value = [convert_func(val) for val in value]                                       # MAIN ERROR 'array'
                    else: 
                        new_value = convert_func(value)                                                     # MAIN 'atomic'
                        if not ('False' in value or 'True' in value):
                            messagebox.showerror("IP : " + self.ip, 'Unexpected value for type BOOL')
                            error = 1
                        elif('False' in value):
                            new_value = False
                else:
                    if(self.elements > 1):
                        value = str(value).strip("[ ]")                                                       # Convert all in class 'list'
                        value = value.split(", ")                                                             #
                        new_value = [convert_func(val) for val in value]                                      # MAIN 'array'
                    else: 
                        new_value = convert_func(value)                                                       # MAIN 'atomic'
            except KeyError:
                messagebox.showerror("IP : " + self.ip, 'Unsupported Data Type')
            except ValueError:
                messagebox.showerror("IP : " + self.ip, 'Invalid Value')
            except Exception as err:
                messagebox.showerror("IP : " + self.ip, f'Unknown Error: {err}')
            else:
                try:
                    #print(type(self.tag))
                    if(self.elements > 1 and error == 0):
                        response = self.plc.write((self.tag + '{' + str((self.plc.tags[self.tag])['dimensions'][0]) + '}' , new_value))
                        self.tag_value.set("Value: " + str(new_value)) 
                    elif(error == 0):
                        response = self.plc.write((self.tag, new_value))
                        self.tag_value.set("Value: " + str(new_value))  
                    if(response and error == 0):
                        messagebox.showinfo("IP : " + self.ip, f'Wrote {response.value!r} to {response.tag}')
                    elif(error == 0):
                        messagebox.showerror("IP : " + self.ip, f'Error writing {new_value!r} to {response.tag}: {response.error}')
                except Exception as err:
                    if(error == 0):
                        messagebox.showerror("IP : " + self.ip, f'Error writing tag: {err}')
        else:
            messagebox.showerror("IP : " + self.ip, 'No Tag Selected')

    def load_tag(self):                                   # function for load my combobox with tag name of all tags
        self.plc.get_tag_list()
        list_tag = []
        for tag in self.plc.tags:
            if((self.plc.tags[tag])['dimensions'] and (self.plc.tags[tag])['dimensions'][0] >= 1):                              #If array
                list_tag.append(self.plc.tags[tag]['tag_name'] + '{' + str((self.plc.tags[tag])['dimensions'][0]) + '}')        #Tag{n}
            else:           
                list_tag.append(self.plc.tags[tag]['tag_name'])                                                                 #Tag
        self.cmb['values'] = sorted(list_tag)
        self.num_tag.set(len(self.cmb['values']))

    def get_tag_datatype(self):
        if self.cmb.get().endswith('}') and '{' in self.cmb.get():
            self.tag, dim = self.cmb.get().split('{')
            self.elements = int(dim[:-1])
        else:
            self.elements = 1
            self.tag = self.cmb.get()
        if((self.plc.tags[self.tag])['tag_type'] == 'struct'):                           
            return (self.plc.tags[self.tag])['data_type']['name']       
        else:          
            return (self.plc.tags[self.tag])['data_type']  

    def click(self, on):
        global i
        if on and i == 1:
            i = 0
        elif not on and i == 0:
            self.led.to_red(True)
            messagebox.showinfo("IP : " + self.ip, "Communication Closed")
            self.parent.destroy()


if __name__ == '__main__':
    root = Tk()
    application = mainapp(root,plc=1)
    root.mainloop()
