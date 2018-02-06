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
    return "{major}.{minor}.{build}".format(
        major=version[0], minor=version[1], build=version[2])


def execute_tests():
    """Execute all tests from DB."""
    print("Getting current records:")
    database_engine.get_current_results()
    logging.info("Executing all tests")
    execution_id = database_engine.record_execution(get_current_os_version())
    # iterate over all tests
    for registrant in database_engine.all_registrants():
        program_id = registrant.id
        # substitute the path into the command
        command = registrant.command.replace('$1', registrant.path)
        # execute the command
        child = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
        # wait for it to finish get an exit code, and get text output
        console_output = child.communicate()[0]
        code = child.returncode
        was_successful = (code == 0)
        database_engine.update_current_record(program_id, execution_id,
                                              was_successful)

        # record all failed executions
        if not was_successful:
            logger.log(logging.DEBUG, "Test {} failed.".format(registrant))
            database_engine.record_failure(program_id, execution_id, code,
                                           console_output)
        print("Test {} exited with code {}".format(registrant, code))
    database_engine.migrate_programs(
    )  # temporary method placement until all coders have migrated

    print("Getting new current records:")  # testing join
    database_engine.get_current_results()


def main():
    # TODO: Get last OS version from DB & compare to current version
    execute_tests()


if __name__ == '__main__':
    main()
