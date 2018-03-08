import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import allamericanregress
import allamericanregress.testing_framework
import allamericanregress.config


logger = allamericanregress.config.logger

class AllAmericanRegressService(win32serviceutil.ServiceFramework):
    """Creates a Windows service that executes the testing framework automatically on boot."""
    _svc_name_ = "regrOS"
    _svc_display_name_ = "regrOS" # display name that appears in Service Manager

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    # How to respond to service stop command
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logger.info('Stopping service ...')
        self.stop_requested = True

    # When launched by service control manager, log brief intro
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    # Executes the tests registered with the application if OS version change detected
    def main(self):
        logger.info(' ** All-American Regress Service running ** ')
        allamericanregress.testing_framework.main()
        return


def install():
    logger.info('Attempting to install.')
    win32serviceutil.HandleCommandLine(
        AllAmericanRegressService, None,
        ["AllAmericanRegressService", "--startup=auto", "install"])
    win32serviceutil.HandleCommandLine(AllAmericanRegressService, None,
                                       ["AllAmericanRegressService", "start"])


if __name__ == '__main__':
    install()
