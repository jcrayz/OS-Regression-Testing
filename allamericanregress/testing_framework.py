from allamericanregress import database_engine
import subprocess
import logging
import sys
if sys.platform == 'linux':
    import allamericanregress.win32api_dummy as win32api
else:
    import win32api
logger = logging.getLogger(__name__)


def get_current_os_version():
    """Get the current version's major.minor.build number"""
    version = win32api.GetVersionEx(1)
    return "{major}.{minor}.{build}".format(major=version[0], minor=version[1], build=version[2])


def execute_tests():
    """Execute all tests from DB."""
    # iterate over all tests
    logging.info("Executing all tests")
    for p in database_engine.all_entries():
        # substitute the path into the command
        command = p[-1].replace('$1', p[2])
        # execute the command
        child = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
        # wait for it to finish get an exit code, and get text output
        console_output = child.communicate()[0]
        code = child.returncode
        # only log if there was an error
        if code != 0:
            logger.log(logging.DEBUG, "Test {} failed.".format(p))
            database_engine.log_executed_test(p[0], console_output, code)
        print("Test {} exited with code {}".format(p, code))


def main():
    # TODO: Get last OS version from DB & compare to current version
    execute_tests()


if __name__ == '__main__':
    main()
