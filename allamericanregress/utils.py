"""Utility functions for AllAmericanRegress"""
import shutil
from allamericanregress import config
import logging
import win32com.shell.shell as shell

logger = logging.getLogger(__name__)


def uninstall():
    """Uninstalls AllAmericanRegress files"""
    print('Uninstalling')
    params = 'sc delete regrOS'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+ params)
    print('done')
    logging.shutdown()
    shutil.rmtree(config.CONFIG_PATH, ignore_errors=True)
    print('Uninstall succeeded')
