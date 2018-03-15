import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging
import time
import subprocess

logging.basicConfig(
    filename='C:\\temp\\service.log',
    level=logging.DEBUG,
    format='[regrOS-service] %(levelname)-7.7s %(message)s'
)

class Service(win32serviceutil.ServiceFramework):
    """Creates a Windows service that executes the testing framework automatically on boot."""
    _svc_name_ = "regrOS"
    _svc_display_name_ = "regrOS" # display name that appears in Service Manager

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        """How to respond to service stop command"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        self.stop_requested = True

    def SvcDoRun(self):
        """When launched by service control manager, log brief intro"""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        logging.info("This is the regrOS service at {}".format(str(time.time())))

        self.main()

    def main(self):
        """Executes the tests registered with the application if OS version change detected"""
        # child = subprocess.Popen(['pipenv', 'run', 'python', '-m', 'allamericanregress', '--list'],
        #                          cwd='C:\\Users\\Jenna\\PycharmProjects\\Capstone')
        child = subprocess.Popen(['pipenv', 'run', 'python', '-m', 'allamericanregress', '--execute-tests'],
                                 cwd='C:\\Users\\Jenna\\PycharmProjects\\Capstone')
        child.wait()
        ret_code = child.returncode
        logging.info("Tests return code: {}".format(str(ret_code)))
        return


def install():
    """Attempts to install program as a Windows service and set it to automatically execute on startup"""
    logging.info('Attempting to install.')
    win32serviceutil.HandleCommandLine(
        Service, None,
        ["regrOS", "--startup=auto", "install"])
    logging.info('Starting service.')
    win32serviceutil.HandleCommandLine(Service, None,
                                       ["regrOS", "start"])


if __name__ == '__main__':
    install()
