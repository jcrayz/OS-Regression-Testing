import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging

# Logs to the temp directory under C
logging.basicConfig(
    filename='C:\\Temp\\hello-service2.log',
    level=logging.DEBUG,
    format='[helloworld2-service] %(levelname)-7.7s %(message)s'
)

# Simple service that logs every 5 seconds 50x
class HelloWorldSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "HelloWorld2-Service"
    _svc_display_name_ = "HelloWorld2 Service"

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
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()

    # Logs "Hello at <time>" 50x at 5 second intervals
    def main(self):
        logging.info(' ** Hello PyWin32 World ** ')
        # Simulate a main loop
        for i in range(0, 50):
            if self.stop_requested:
                logging.info('A stop signal was received: Breaking main loop ...')
                break
            time.sleep(5)
            logging.info("Hello at %s" % time.ctime())
        return


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(HelloWorldSvc, None, ["HelloWorldSvc","--startup=auto", "install"])
    win32serviceutil.HandleCommandLine(HelloWorldSvc, None, ["HelloWorldSvc", "start"])