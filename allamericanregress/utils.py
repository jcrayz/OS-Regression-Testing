"""Utility functions for AllAmericanRegress"""
import shutil
from allamericanregress import config
import logging
import sys
import win32com.shell.shell as shell

logger = logging.getLogger(__name__)


def uninstall():
    """Uninstalls AllAmericanRegress files"""
    # TODO: Uninstall the service
    print('Uninstalling')
    params = 'sc delete regrOS'
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable,
                         lpParameters=params)
    print('done')
    logging.shutdown()
    shutil.rmtree(config.CONFIG_PATH, ignore_errors=True)
    print('Uninstall succeeded')
