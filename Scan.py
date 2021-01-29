import win32api
import re
import wmi
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


root = Tk()
root.title('ScanService.exe')
root.iconbitmap("Detect.ico")
root.geometry("550x380")
root.config(background='#d3e0ea')
root.resizable(0, 0)


def getFileProperties(fname):

    """
    Read all properties of the given file return them as a dictionary.
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo
    except:
        pass

    return props


def end():
    exit()


def remove(sel):
    global bt2
    c = wmi.WMI()
    bt3.destroy()
    for service in c.Win32_service():
        if service.name == sel or service.pathname == sel:
            service.StopService()
            service.Delete()
            print('Done')
    bt2.config(text='Terminé', command=end)


def on_click(event):
    global suspect
    global sel
    index = suspect.curselection()
    sel = suspect.get(index)


def scan():
    global suspect
    global sel
    global bt3
    global bt2
    root.geometry("750x300")
    label1.place(x=150, y=20)
    label2.destroy()
    bt.destroy()
    # list des path des services
    serp = []
    # list des noms des services
    sern = []
    suspect=Listbox(root, width=100, height=10)
    c = wmi.WMI()
    for service in c.Win32_Service():
        # not set to None
        if service.pathname:
            if re.match('[A-Za-z]*\.exe$', os.path.split(service.pathname)[1].replace('\"', '')):
                sern.append(service.name)
                serp.append(service.pathname.replace('\"', ''))
    nb=0
    for i in serp:
        for n in getFileProperties(i).keys():
            if n == 'StringFileInfo':
                if not getFileProperties(i).get(n) or not getFileProperties(i).get(n).get('CompanyName'):
                    j = serp.index(i)
                    suspect.insert(END, sern[j])
                    suspect.insert(END, 'path: '+serp[j])

    suspect.place(x=30, y=100)
    suspect.bind('<ButtonRelease-1>', on_click)
    bt2 = Button(root, text='Remove', font=('Verdana', 10, 'bold'), relief=FLAT, fg='#f1f6f9', bg='#14274e',
                 command=lambda: remove(sel))
    bt2.place(x=650, y=150)
    bt3 = Button(root, text='Cancel', font=('Verdana', 10, 'bold'), relief=FLAT, fg='#f1f6f9', bg='#14274e',
                 command=end)
    bt3.place(x=650, y=200)


label1 = Label(root, text="Bienvenue dans le ScanService", font=('Verdana', 18, 'bold'), fg='#0a043c', bg='#d3e0ea')
label1.place(x=70, y=20)
label2 = Label(root, text="Ce programme va scanner tous vos services windows\n"
                          " a la recherche des services malicieux", font=('Verdana', 10), fg='black', bg='#d3e0ea')
label2.place(x=105, y=80)

bt=Button(root, text='Click to Scan', font=('Verdana', 10, 'bold'), width=30, height=3, border=3, relief=FLAT,
          bg='#16c79a', command=scan)
bt.place(x=140, y=180)
root.mainloop()
