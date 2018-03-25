import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import subprocess
import sqlite3
import sys
import os
import win32com.shell.shell as shell

logging.basicConfig(
    filename='C:\\temp\\regrOS.log',
    level=logging.DEBUG,
    format='[regrOS-service] %(levelname)-7.7s %(message)s'
)

class RegrOSService(win32serviceutil.ServiceFramework):
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
        self.main()

    def main(self):
        """Executes the tests registered with the application if OS version change detected"""
        logging.info(' ** Running test suites ** ')
        # TODO: Move check OS version code to this class
        self.execute_tests()
        time.sleep(30)
        return

    def execute_tests(self):
        """Execute all tests from DB."""
        # iterate over all tests
        try:
            logging.info('* * Reached execute_tests * *')
            CONFIG_PATH = os.path.join('c:/', 'AllAmericanRegress')
            DB_PATH = os.path.join(CONFIG_PATH, 'aar_db.db')
            database_connection = sqlite3.connect(DB_PATH)
            cursor = database_connection.cursor()
            for p in cursor.execute("""SELECT * FROM registrant"""):
                # substitute the path into the command
                command = p[2].replace('$1', p[1])
                # execute the command
                child = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
                # wait for it to finish get an exit code, and get text output
                console_output = child.communicate()[0]
                code = child.returncode
                # only log if there was an error
                if code != 0:
                    logging.debug("Test {} failed.".format(p[3]))
                    # database_engine.log_executed_test(p[0], console_output, code)
                logging.info("Test {} exited with code {}".format(p[3], code))
                # TODO: record the execution, any failures, and update current records
        except Exception as e:
            logging.exception(str(e))


if __name__ == '__main__':
    """Installs the service using admin privileges. Privilege code taken from Jorenko's answer at
    https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script#answer-11746382"""
    ASADMIN = "--asadmin"
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])  # get current execution command
        new_args = sys.argv[1:] + [ASADMIN]  # add admin arg to avoid infinite recursion
        params = ' '.join([script] + new_args)
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)  # relaunch as admin
    else:
        win32serviceutil.HandleCommandLine(RegrOSService, None,
                                           ["regrOS", "--startup=auto", "install"])
        win32serviceutil.HandleCommandLine(RegrOSService, None, ["regrOS", "start"])

