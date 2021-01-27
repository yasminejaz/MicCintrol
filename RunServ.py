import win32con
import win32service


def ListServices():

    accessSCM = win32con.GENERIC_READ
    accessSrv = win32service.SC_MANAGER_ALL_ACCESS

    # Open Service Control Manager
    hscm = win32service.OpenSCManager(None, None, accessSCM)

    # Enumerate Service Control Manager DB
    typeFilter = win32service.SERVICE_WIN32_OWN_PROCESS # Le type de service de notre fake service
    stateFilter = win32service.SERVICE_STATE_ALL

    statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)

    for (short_name, desc, status) in statuses:
        if status[1]==4: # if running 
            print(short_name, status)


ListServices()
