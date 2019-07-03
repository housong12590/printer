import win32serviceutil
import win32service
import win32event
import win32timezone
import os


class WinService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'printer_repeater'
    _svc_display_name_ = 'printer_repeater'
    _svc_description_ = '打印转发服务'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.run = True

    def SvcDoRun(self):
        from printer_repeater import main
        main()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.run = False


if __name__ == '__main__':
    import sys
    import servicemanager

    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(WinService)  # 如果修改过名字，名字要统一
            servicemanager.Initialize('WinService', evtsrc_dll)  # 如果修改过名字，名字要统一
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror

            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(WinService)  # 如果修改过名字，名字要统一
