import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import allamericanregress
import allamericanregress.testing_framework

# Logs to the temp directory under C
logging.basicConfig(
    filename='C:\\Temp\\allamericanregress.log',
    level=logging.DEBUG,
    format='[allamericanregress-service] %(levelname)-7.7s %(message)s')


# Simple service that logs every 5 seconds 50x
class AllAmericanRegressService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AllAmericanRegress"
    _svc_display_name_ = "OS Regression Testing"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    # How to respond to service stop command
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        self.stop_requested = True

    # When launched by service control manager, log brief intro
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    # Logs "Hello at <time>" 50x at 5 second intervals
    def main(self):
        logging.info(' ** Running test suites ** ')
        allamericanregress.testing_framework.execute_tests()
        return

def install():
    win32serviceutil.HandleCommandLine(
        AllAmericanRegressService, None,
        ["AllAmericanRegressService", "--startup=auto", "install"])
    win32serviceutil.HandleCommandLine(AllAmericanRegressService, None,
                                       ["AllAmericanRegressService", "start"])
    
if __name__ == '__main__':
    install()
