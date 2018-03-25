"""Testing framework for regrOS"""
from allamericanregress import database_engine
import subprocess
import logging
import sys
import os

# Determines if the system is linux or windows to execute the proper import
if sys.platform == 'linux':
    import allamericanregress.win32api_dummy as win32api
else:
    import win32api
logger = logging.getLogger(__name__)


def get_current_os_version():
    """Get the current version's major.minor.build number"""
    version = win32api.GetVersionEx(1)
    return "{major}.{minor}.{build}".format(
        major=version[0], minor=version[1], build=version[2])


def execute_tests():
    """Execute all tests from DB."""
    logger.disabled = False
    logger.info("Executing all tests")
    if logger.disabled:
        raise RuntimeError('logger is disabled but shouldn\'t be')
    execution_id = database_engine.record_execution(get_current_os_version())
    # iterate over all tests
    for registrant in database_engine.all_registrants():
        program_id = registrant.id
        # substitute the path into the command
        command_path = str(registrant.command).replace('$1', registrant.path)
        # execute the command
        try:
            print('args: {}'.format(command_path))
            child = subprocess.Popen(command_path, stdout=subprocess.PIPE)
            # wait for it to finish get an exit code, and get text output
            console_output = child.communicate()[0]
            code = child.returncode
        except FileNotFoundError:
            code = 1
            console_output = ''

        # tests pass if the exit code was 0
        was_successful = (code == 0)
        database_engine.update_current_record(program_id, execution_id,
                                              was_successful)

        # record all failed executions
        if not was_successful:
            logger.log(logging.DEBUG, "Test {} failed.".format(registrant))
            database_engine.record_failure(program_id, execution_id, code,
                                           console_output)
        print("Test {} exited with code {}".format(registrant, code))


def main():
    f = open('C:\\temp\\debug.log', 'a')
    f.write('In testing framework main\n')
    f.close()
    """Checks the last recorded OS version against the current version, and executes tests if it changed."""
    last_tested_version = database_engine.get_last_os_version()
    current_version = get_current_os_version()
    if (last_tested_version is not current_version):
        logger.log("Detected version change from {} to {}".format(
            last_tested_version, current_version))
        execute_tests()
    else:
        logger.log("No version change detected. Tests will not be executed.")
    f = open('C:\\temp\\debug.log', 'a')
    f.write('Finished testing framework main\n')
    f.close()


if __name__ == '__main__':
    main()
