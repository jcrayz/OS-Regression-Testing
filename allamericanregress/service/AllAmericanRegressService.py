"""Windows service for executing registered tests on boot when an update occurred."""
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import subprocess
import sys
import os
import win32com.shell.shell as shell
import service_database_engine
import shlex
logging.basicConfig(
    filename=service_database_engine.LOG_PATH,
    level=logging.DEBUG,
    format=service_database_engine.LOG_FORMAT
)


class RegrOSService(win32serviceutil.ServiceFramework):
    """Creates a Windows service that executes the testing framework automatically on boot."""
    _svc_name_ = "regrOS"
    _svc_display_name_ = "regrOS"  # display name that appears in Service Manager

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
        logging.info(' ** Checking for update ** ')
        last_tested_version = service_database_engine.get_last_os_version()
        current_version = self.get_current_os_version()
        if (last_tested_version == current_version) and False:
            logging.info(' ** No update detected. Tests will not be run. **')
        else:
            logging.info(' ** Version changed from {old} to {new}. Running tests.'
                         .format(old=last_tested_version, new=current_version))
            self.execute_tests()
        time.sleep(30)
        return

    def get_current_os_version(self):
        """Get the current OS version"""
        import platform
        version = platform.platform()
        return version

    def execute_tests(self):
        """Execute all tests from DB."""
        # iterate over all tests
        try:
            logging.info('* * Locate pipenv command * *')
            # child = subprocess.Popen(['pipenv','run','allamericanregress','--execute-tests'],cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))), stdout=subprocess.PIPE)
            child = subprocess.Popen(
                ['where', 'pipenv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # wait for it to finish get an exit code, and get text output
            console_output = child.communicate()
            code = child.returncode
            logging.info('console output: %s', console_output)
            # ========== Try to install pipenv env ==========
            logging.info('* * pipenv install * *')
            env_path = os.path.dirname(
                os.path.dirname(os.path.dirname(__file__)))
            logging.info('path=%s', env_path)
            cmd = shlex.split('python -m pipenv install')
            logging.info('cmd=%s', cmd)
            child = subprocess.Popen(
                cmd, cwd=env_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            console_output = child.communicate()
            code = child.returncode
            logging.info('pipenv: code=%s, output=%s',
                         code, console_output)
            # ========== Execute tests ==========
            logging.info('* * Executing tests * *')
            logging.info('execute tests via console')
            cmd = shlex.split(
                'python -m pipenv run python -m allamericanregress --execute-tests')
            logging.info('cmd=%s', cmd)
            child = subprocess.Popen(
                cmd, cwd=env_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            console_output = child.communicate()
            code = child.returncode
            logging.info('pipenv: code=%s, output=%s',
                         code, console_output)
            logging.info('execute tests via lib')
            execution_id = service_database_engine.record_execution(
                self.get_current_os_version())
            for p in service_database_engine.get_registrants():
                # substitute the path into the command
                command = p[2].replace('$1', p[1])
                # execute the command
                try:
                    child = subprocess.Popen(command, stdout=subprocess.PIPE)
                    # wait for it to finish get an exit code, and get text
                    # output
                    console_output = child.communicate()[0]
                    code = child.returncode
                except FileNotFoundError:
                    code = 1
                    console_output = "File not found."
                was_successful = (code == 0)
                # update registrant's current record
                service_database_engine.update_current_record(
                    p[0], execution_id, was_successful)
                # record all failures
                if not was_successful:
                    logging.debug("Test {} failed.".format(p[3]))
                    service_database_engine.record_failure(
                        p[0], execution_id, code, "")
                logging.debug("Test {} exited with code {}".format(p[3], code))
        except Exception as e:
            logging.exception(str(e))


if __name__ == '__main__':
    """Installs the service using admin privileges. Privilege code taken from Jorenko's answer at
    https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script#answer-11746382"""
    ASADMIN = "--asadmin"
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])  # get current execution command
        # add admin arg to avoid infinite recursion
        new_args = sys.argv[1:] + [ASADMIN]
        params = ' '.join([script] + new_args)
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable,
                             lpParameters=params)  # relaunch as admin
    else:
        win32serviceutil.HandleCommandLine(RegrOSService, None,
                                           ["regrOS", "--startup=auto", "install"])
        win32serviceutil.HandleCommandLine(
            RegrOSService, None, ["regrOS", "start"])
