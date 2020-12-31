import win32api
import win32gui
import sounddevice as sd
from scipy.io.wavfile import write


#On teste si le Mic est eteint
fs = 44100 #fréquence d'échantillonnage
sec = 10 #durée de l'enregistrement
print("10sec")
record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
sd.wait()

if (record[440998][0]==3.0517578125e-05 and record[440998][1]==0.0 and record[440999][0]==0.0 and record[440999][1]== -3.0517578125e-05): #On teste les vals recup avec les vals du record dans le cas Mute Mic
    print("Unmute Mic Starting .....")
    WM_APPCOMMAND = 0x319
    APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
    print("Mic is On")
    ###########################################
    print("Start Recording ....")
    fs = 44100  # fréquence d'échantillonnage
    sec = 30  # durée de l'enregistrement 30sec
    record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output.wav', fs, record)

else:
    print("Mic is On")
    print("Recording Starting .....")
    fs = 44100  # fréquence d'échantillonnage
    sec = 30  # durée de l'enregistrement 30sec
    record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output.wav', fs, record)
print("End")


