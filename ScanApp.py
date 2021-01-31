import win32api
import wmi
import os
from tkinter import *
import smtplib
from datetime import datetime
import socket
from columnar import columnar
from email.header import Header
from email.utils import formataddr
from email.message import EmailMessage
from validate_email import validate_email


root = Tk()
root.title('ScanService.exe')
root.iconbitmap("Detect.ico")
root.geometry("550x380")
root.config(background='#d3e0ea')
root.resizable(0, 0)

sender = 'testhomeworkos@gmail.com'
receiver = ''
password = 'Testhomeworkos1'
machine = socket.gethostname()
date = datetime.now()


# ********************************* SEND EMAIL TO USER
def envoiMail(sender,receiver,susm):

    msg = EmailMessage()
    msg['From'] = formataddr((str(Header('ScanService', 'utf-8')), sender))
    msg['To'] = receiver
    text = "Bonjour cher client,\n\n" \
           "Merci d'avoir utiliser notre service de detection des services windows malicieux.\n" \
           "Voici le rapport du scan sur votre machine: " + machine + "\nEffectué le: " + str(date) + \
           "\n\n" + columnar(susm, headers=['Service Name:'], no_borders=True)
    msg.set_content(text)
    msg['Subject'] = 'Rapport Scan Service'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg, sender)
    server.quit()


# ******************************** GET SERVICE PROPERTIES
def getFileProperties(fname):
    # Read all properties of the given file return them as a dictionary.

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

        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo

    except:
        pass

    return props


def end():
    exit()


# ******************************** REMOVE SELECTED SERVICE
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


# ******************************** GET SELECTED SERVICE
def on_click(event):
    global suspect
    global sel
    index = suspect.curselection()
    sel = suspect.get(index)


# ******************************* GET MAIL
def getmail():
    global email
    global receiver
    receiver = email.get()


# ******************************* SCAN
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
    susm=[]
    suspect = Listbox(root, width=100, height=10, relief=FLAT)
    c = wmi.WMI()
    for service in c.Win32_Service():
        # not set to None
        if service.pathname:
            if re.match('[A-Za-z0-9]*\.exe$', os.path.split(service.pathname)[1].replace('\"', '')):
                sern.append(service.name)
                serp.append(service.pathname.replace('\"', ''))
    for i in serp:
        for n in getFileProperties(i).keys():
            if n == 'StringFileInfo':
                if not getFileProperties(i).get(n) or not getFileProperties(i).get(n).get('CompanyName'):
                    j = serp.index(i)
                    suspect.insert(END, sern[j])
                    suspect.insert(END, 'path: '+serp[j])
                    susm.append([sern[j]])

    if receiver != '' and validate_email(receiver):
        envoiMail(sender, receiver, susm)

    suspect.place(x=30, y=100)
    suspect.bind('<ButtonRelease-1>', on_click)
    label5 = Label(root, text='Liste des services suspects:', font=('Verdana', 13, 'bold'), bg='#d3e0ea')
    label5.place(x=30, y=70)
    bt2 = Button(root, text='Remove', font=('Verdana', 10, 'bold'), relief=FLAT, fg='#f1f6f9', bg='#14274e',
                 command=lambda: remove(sel))
    bt2.place(x=650, y=150)
    bt3 = Button(root, text='Cancel', font=('Verdana', 10, 'bold'), relief=FLAT, fg='#f1f6f9', bg='#14274e',
                 command=end)
    bt3.place(x=650, y=200)

################################################# INTERFACE ############################################################


label1 = Label(root, text="Bienvenue dans le ScanService", font=('Verdana', 18, 'bold'), fg='#0a043c', bg='#d3e0ea')
label1.place(x=70, y=20)
label2 = Label(root, text="Ce programme va scanner tous vos services windows\n"
                          " a la recherche des services malicieux", font=('Verdana', 10), fg='black', bg='#d3e0ea')
label2.place(x=105, y=60)
can=Canvas(root, width=450, height=250, highlightthickness=0, relief='ridge')
can.create_rectangle(0, 0, 450, 250, fill='#d3e0ea', outline='')
can.place(x=50,y=110)
label3 = Label(root, text='Pour recevoir un rapport du scan par e-mail', font=('Verdana', 8), fg='black', bg='#d3e0ea')
label3.place(x=95, y=150)
label4 = Label(root, text='Veuillez introduire votre addresse:', font=('Verdana', 8), fg='black', bg='#d3e0ea')
label4.place(x=95, y=170)
email = StringVar()
mail = Entry(root, textvariable=email, width=50, command=getmail())
mail.place(x=100, y=190)
btm = Button(root, text='Submit', font=('Verdana', 8, 'bold'), relief=FLAT, bg='#16c79a', command=getmail)
btm.place(x=430, y=190)
bt = Button(root, text='Click to Scan', font=('Verdana', 10, 'bold'), width=30, height=3, border=3, relief=FLAT,
          bg='#16c79a', command=scan)
bt.place(x=140, y=280)
root.mainloop()
