import shutil
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import time
import datetime

root = Tk()
root.title('AllBCKUP')
root.geometry('600x300')

c = Canvas(root, height=500, width=1500)
c.place(relwidth=1, relheight=1)

global SavePath
SavePath = ''

global LoadPath
LoadPath = ''



current_hour = str(datetime.datetime.now())[0:13]
hour = current_hour[11:13]
last_hour = current_hour[0:11] + str(int(hour) - 1)




# Pobiera aktualną datę i tworzy na jej podstawie nazwe folderu
def GetDirName():
    date = str(datetime.datetime.now())
    DirName = date[0:10] + '___' + date[11:13] + '.' + date[14:16]
    return DirName


def SearchPath():
    global FilePath
    FilePath = filedialog.askdirectory()
    name = GetDirName()
    global SavePath
    SavePath = str(FilePath + "\\" + name)

    TargetLabel = Label(c, text='Kopiuję do:     ' + str(FilePath))
    TargetLabel.pack()
    TargetLabel.place(relwidth=1, relheight=0.1, rely=0.9)


x = GetDirName()
print(current_hour)


def SourcePath():
    global LoadPath
    LoadPath = filedialog.askdirectory()
    SourceLabel = Label(c, text='Kopiuję z:     ' + str(LoadPath))
    SourceLabel.pack()
    SourceLabel.place(relwidth=1, relheight=0.1, rely=0.8)
    print(n.get())


def GetFiles():
    global FilesList
    FilesList = [f for f in os.listdir(LoadPath) if os.path.isfile(os.path.join(LoadPath, f))]


def DoBackup():
    global FilesList
    FilesList = [f for f in os.listdir(LoadPath) if os.path.isfile(os.path.join(LoadPath, f))]

    name = GetDirName()
    global SavePath
    SavePath = str(FilePath + "\\" + name)

    NewDirectory = str(os.makedirs(SavePath))

    current_hour = str(datetime.datetime.now())[0:13]
    hour = current_hour[11:13]
    last_hour = current_hour[0:11] + str(int(hour) - 1)

    for f in FilesList:
        Path = str(LoadPath + "\\" + f)
        ModDate = str(datetime.datetime.fromtimestamp(os.path.getmtime(Path)))[0:13]


        if ModDate == current_hour or last_hour:
            GetFile = shutil.copy(Path, SavePath)
            print(Path)
            print(NewDirectory)

    if not os.listdir(SavePath):
        os.rmdir(SavePath)


def MainProces():
    if n.get() == 'Wybierz interwał zapisu':
        messagebox.showinfo("Info", n.get())

    if n.get() == '30 minut':
        print('30m')
        while True:
            DoBackup()
            time.sleep(1800)

    elif n.get() == '1 godzina':
        print('1h')
        while True:
            DoBackup()
            time.sleep(3600)

    elif n.get() == '2 godziny':
        print('2h')
        while True:
            DoBackup()
            time.sleep(7200)

    elif n.get() == '4 godziny':
        print('4h')
        while True:
            DoBackup()
            time.sleep(14400)




# frame = Frame(root) # ramka
# frame.grid(row=0, column=1 )
# frame.config(background='black')


# c.config(background='#2c3440') # manipulacja płótnem


# Combobox creation
n = StringVar()
Delay = ttk.Combobox(c, width=27, font='calibri', textvariable=n)
Delay.pack()
Delay.place(relwidth=1, relheight=0.2, rely=0)

# global choose
# Delay.bind("Wybierz interwał zapisu", choose = 0)

# Adding combobox drop down list
Delay['values'] = ('Wybierz interwał zapisu', '30 minut', '1 godzina', '2 godziny', '4godziny')
Delay.current(0)

TPath = Button(c, text='Dokąd kopiować?', font='calibri', border=5, command=SearchPath)
TPath.place(relwidth=1, relheight=0.2, rely=0.4)

SPath = Button(c, text='Skąd kopiować?', font='calibri', border=5, command=SourcePath)
SPath.pack()
SPath.place(relwidth=1, relheight=0.2, rely=0.2)

# testowy = Button(c,text='GetFiles', command=GetFiles)
# testowy.pack()

Backup = Button(c, text='ROZPOCZNIJ', font='calibri', border=5, command=MainProces)
Backup.pack()
Backup.place(relwidth=1, relheight=0.2, rely=0.6)




# path =


#


# os.makedirs(SavePath)


root.mainloop()