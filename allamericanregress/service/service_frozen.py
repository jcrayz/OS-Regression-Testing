"""Frozen version of the service
Windows service for executing registered tests on boot when an update occurred."""

# based off of this: https://www.codeproject.com/Articles/1115336/Using-Python-to-Make-a-Windows-Service
import win32serviceutil
import win32service
import win32event
import win32timezone
import servicemanager
import socket
import time
import logging
import subprocess
import sys
import os
import win32com.shell.shell as shell
import shlex
import sys
import contextlib

to_append = os.path.dirname(os.path.dirname(__file__))
sys.path.append(to_append)


CONFIG_PATH = os.path.join('c:/', 'AllAmericanRegress')
LOG_PATH = os.path.join(CONFIG_PATH, 'service.log')
LOG_FORMAT = '[regrOS-service] %(asctime)s %(levelname)-7.7s %(message)s'


FROZEN = getattr(sys, 'frozen', False)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format=LOG_FORMAT
)

logger = logging.getLogger(__name__)


def execute_tests():
    """Execute all tests from DB."""
    logger.info('Service is executing tests.')
    try:
        logger.info('Execute tests as frozen dist')

        args = ([os.path.join(os.path.dirname(
                os.path.abspath(sys.executable)), 'regros', 'regros.exe'), '--execute-tests'],)
        # args = (['dir'],)
        kwargs = dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        logger.info(
            'Calling regros.exe with args: args=%s kwargs=%s', args, kwargs)
        # logger.info('Files in dir. cwd=%s files=%s', kwargs[
        #             'cwd'], os.listdir(kwargs['cwd']))
        child = subprocess.Popen(*args, **kwargs)
        console_output = child.communicate()
        code = child.returncode
        logger.info('Tests output: %s', console_output)

    except Exception as e:
        logger.exception(str(e))
        raise e


class RegrOSService(win32serviceutil.ServiceFramework):
    """Creates a Windows service that executes the testing framework automatically on boot."""
    _svc_name_ = "regrOS"
    # display name that appears in Service Manager
    _svc_display_name_ = "regrOS regresssion testing"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True

    def SvcStop(self):
        """How to respond to service stop command"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logger.info('Stopping service ...')

    def SvcDoRun(self):
        """When launched by service control manager, log brief intro"""
        logger.info('SvcDoRun')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        # rc = None
        # while rc != win32event.WAIT_OBJECT_0:
        #     rc = win32event.WaitForSingleObject(self.stop_event, 5000)

    def main(self):
        """Executes the tests registered with the application if OS version change detected"""
        # logger.info(' ** Checking for update ** ')
        # last_tested_version = service_database_engine.get_last_os_version()
        # current_version = self.get_current_os_version()
        # if (last_tested_version == current_version):
        #     logger.info(' ** No update detected. Tests will not be run. **')
        # else:
        #     logger.info(' ** Version changed from {old} to {new}. Running tests.'
        #                  .format(old=last_tested_version, new=current_version))
        logger.info(' ** Executing tests ** ')
        execute_tests()
        # time.sleep(30)
        while rc != win32event.WAIT_OBJECT_0:
            # block for 5 seconds and listen for a stop event
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
        return

    def get_current_os_version(self):
        """Get the current OS version"""
        import platform
        version = platform.platform()
        return version


def install_commandline():
    logger.info('main()-admin Service is admin')
    rs = []
    try:
        logger.info('first win32serviceutil.HandleCommandLine')
        c = win32serviceutil.HandleCommandLine(RegrOSService, None,
                                               ["regrOS", "--startup=auto", "install"])
        logger.info('second win32serviceutil.HandleCommandLine')
        rs.append(c)
        # this function behaves as expected if called with "debug" instead of
        # start
        c = win32serviceutil.HandleCommandLine(
            RegrOSService, None, ["regrOS", "start"])
        rs.append(c)
        logger.info('finished win32serviceutil.HandleCommandLine commands')
        logger.info(
            'Service win32serviceutil.HandleCommandLine return codes: %s', rs)
        logger.info('Process did not die while installing')
    except SystemExit:
        logger.info('Process died while installing')


def main():
    """Installs the service using admin privileges. Privilege code taken from Jorenko's answer at
    https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script#answer-11746382"""
    logger.info('Service main running as frozen dist.')
    logger.info('Service called with args: %s', sys.argv)
    with open(LOG_PATH, 'a') as f:
        # cause calls to print() to be written to a file
        with contextlib.redirect_stdout(f):
            # the Windows Service framework calls this executable with no args.
            if len(sys.argv) == 1:
                servicemanager.Initialize()
                servicemanager.PrepareToHostSingle(RegrOSService)
                servicemanager.StartServiceCtrlDispatcher()
            else:
                win32serviceutil.HandleCommandLine(RegrOSService)


if __name__ == '__main__':
    logger.info('Service is main')
    main()
