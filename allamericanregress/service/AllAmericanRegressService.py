"""Windows service for executing registered tests on boot when an update occurred."""
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
# import service_database_engine
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
        logger.info('* * Locate pipenv command * *')
        # child = subprocess.Popen(['pipenv','run','allamericanregress','--execute-tests'],cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))), stdout=subprocess.PIPE)
        child = subprocess.Popen(
            ['where', 'pipenv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # wait for it to finish get an exit code, and get text output
        console_output = child.communicate()
        code = child.returncode
        logger.info('console output: %s', console_output)
        # ========== Try to install pipenv env ==========
        logger.info('* * pipenv install * *')
        # TODO: Use Frozen path
        env_path = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__)))
        logger.info('path=%s', env_path)
        cmd = shlex.split('python -m pipenv install')
        logger.info('cmd=%s', cmd)
        child = subprocess.Popen(
            cmd, cwd=env_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        console_output = child.communicate()
        code = child.returncode
        logger.info('pipenv: code=%s, output=%s',
                    code, console_output)
        # ========== Execute tests ==========
        logger.info('* * Executing tests * *')
        logger.info('execute tests via console')
        cmd = shlex.split(
            'python -m pipenv run python -m allamericanregress --service-execute-tests')
        logger.info('cmd=%s', cmd)
        child = subprocess.Popen(
            cmd, cwd=env_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        console_output = child.communicate()
        code = child.returncode
        logger.info('pipenv: code=%s, output=%s',
                    code, console_output)
    except Exception as e:
        logger.exception(str(e))
        raise e


class RegrOSService(win32serviceutil.ServiceFramework):
    """Creates a Windows service that executes the testing framework automatically on boot."""
    _svc_name_ = "regrOS"
    _svc_display_name_ = "regrOS"  # display name that appears in Service Manager

    def __init__(self, args):
        super().__init__(self, args)
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False
        # self.FROZEN = FROZEN

    def SvcStop(self):
        """How to respond to service stop command"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logger.info('Stopping service ...')
        self.stop_requested = True

    def SvcDoRun(self):
        """When launched by service control manager, log brief intro"""
        logger.info('SvcDoRun')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            rc = win32event.WaitForSingleObject(self.stop_event, 5000)

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
        return

    def get_current_os_version(self):
        """Get the current OS version"""
        import platform
        version = platform.platform()
        return version


def main():
    """Installs the service using admin privileges. Privilege code taken from Jorenko's answer at
    https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script#answer-11746382"""
    logger.info('Service main running as frozen dist.')
    logger.info('Service called with args: %s', sys.argv)

    # win32serviceutil.HandleCommandLine(RegrOSService,argv=sys.argv)
    logger.disabled = False
    # use this cmd line option in roder to get usage() output
    # to check if args are invalid

    if not shell.IsUserAnAdmin():
        logger.info('Service is not admin')
        script = os.path.abspath(sys.argv[0])  # get current execution command
        # add admin arg to avoid infinite recursion
        new_args = sys.argv[1:]
        params = ' '.join([script] + new_args)
        logger.info('Source dist rerun as admin params: %s', params)
        logger.info(f'params: {params}')
        logger.info(f'sys.executable: {sys.executable}\n')
        val = shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable,
                                   lpParameters=params)  # relaunch as admin
        logger.info('ShellExecuteEx returned this: %s', type(val['hProcess']))

    else:
        logger.info('Service is admin')
        logger.info('Delegate to win32serviceutil.HandleCommandLine')
        with open(LOG_PATH, 'a') as f:
            with contextlib.redirect_stdout(f):
                win32serviceutil.HandleCommandLine(
                    RegrOSService, None, sys.argv)


if __name__ == '__main__':
    logger.info('Service is main')
    main()
