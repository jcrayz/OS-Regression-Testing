import win32api
import os
import sys
import win32com.shell.shell as shell
import logging
import time
ASADMIN = '--asadmin'
import allamericanregress.AllAmericanRegressService

"""Code taken from Jorenko's answer at
https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script#answer-11746382"""
def testing():
    # Logs to the temp directory under C
    print('hello, i am in testing')
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        new_args = sys.argv[1:] + [ASADMIN]
        f = open('C:\\temp\\jennatest.log', 'a')
        f.write('\nOpened log file~sys.executable={}'.format(sys.executable))
        f.write('\nscript={script}\nparams={params}'.format(script=script, params=new_args))
        f.close()
        params = ' '.join([script] + new_args)
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        # sys.exit(0)
    else:
        f = open('C:\\temp\\jennatest.log', 'a')
        f.write('\nREACHED ELSE!  THIS IS A BIG DEAL!')
        f.close()
        allamericanregress.AllAmericanRegressService.install()

    # version = win32api.GetVersionEx(1)
    # major = version[0]
    # minor = version[1]
    # build = version[2]
    # print("Version {major}.{minor}.{build}".format(major=major, minor=minor, build=build))
    # print("{major}.{minor}.{build}".format(major = version[0], minor = version[1], build = version[2]))