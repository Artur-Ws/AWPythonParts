import shutil
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import time
import datetime

root = Tk()
root.title('AutoBackup for Allplan')
root.geometry('600x300')

c = Canvas(root, height=500, width=1500)
c.place(relwidth=1, relheight=1)

class PathUtil:

    def __init__(self):
        pass


class Backup:


    def search_file(self):
        pass

    def should_be_copied(self, file, interval, factor, path):
        """ Return True if input file was edited since last backup, otherwise return false """

        file_path = str(path + "\\" + file)

        current_hour = str(datetime.datetime.now())[11:13]
        current_minute = str(datetime.datetime.now())[14:16]
        current_time_in_minutes = int(current_hour) * 60 + int(current_minute)

        file_mod_hour = str(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))[11:13]
        file_mod_minute = str(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))[14:16]
        file_mod_time_in_minutes = int(file_mod_hour) * 60 + int(file_mod_minute)

        if file_mod_time_in_minutes > current_time_in_minutes - interval - factor:
            return True
        else:
            return False

    def search_path(self):
        """ Open choose save directory dialog window, return save path """

        file_path = filedialog.askdirectory()
        name = str(datetime.datetime.now())[0:10]
        save_path = str(file_path + "\\" + name)

        target_label = Label(c, text='Kopiuję do:     ' + str(file_path))
        target_label.pack()
        target_label.place(relwidth=1, relheight=0.1, rely=0.9)

        return save_path

    def source_path(self):
        """ Open choose save directory dialog window, return save path """

        load_path = filedialog.askdirectory()

        SourceLabel = Label(c, text='Kopiuję z:     ' + str(load_path))
        SourceLabel.pack()
        SourceLabel.place(relwidth=1, relheight=0.1, rely=0.8)

        return load_path

    def graphic_interface(self):

        n = StringVar()
        Delay = ttk.Combobox(c, width=27, font='calibri', textvariable=n)
        Delay.pack()
        Delay.place(relwidth=1, relheight=0.2, rely=0)

        # global choose
        # Delay.bind("Wybierz interwał zapisu", choose = 0)

        # Adding combobox drop down list
        Delay['values'] = ('Wybierz interwał zapisu', '30 minut', '1 godzina', '2 godziny', '4godziny')
        Delay.current(0)

        target_path = Button(c, text='Dokąd kopiować?', font='calibri', border=5, command=self.search_path)
        target_path.place(relwidth=1, relheight=0.2, rely=0.4)

        SPath = Button(c, text='Skąd kopiować?', font='calibri', border=5, command=self.source_path)
        SPath.pack()
        SPath.place(relwidth=1, relheight=0.2, rely=0.2)

        # testowy = Button(c,text='GetFiles', command=GetFiles)
        # testowy.pack()

        # Backup = Button(c, text='ROZPOCZNIJ', font='calibri', border=5, command=MainProces)
        # Backup.pack()
        # Backup.place(relwidth=1, relheight=0.2, rely=0.6)
        #
        # root.mainloop()
 x = Backup()
x.graphic_interface()