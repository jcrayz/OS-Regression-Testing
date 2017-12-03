from allamericanregress import database_engine
import subprocess
import logging
logger = logging.getLogger(__name__)


def execute_tests():
    for p in database_engine.all_entries():
        command = p[-1].replace('$1', p[2])
        child = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
        console_output = child.communicate()[0]
        code = child.returncode
        if code != 0:
            logger.log(logging.DEBUG, "Test {} failed.".format(p))
            database_engine.log_executed_test(p[0], console_output, code)
        print("Test {} exited with code {}".format(p, code))


def main():
    execute_tests()


if __name__ == '__main__':
    main()
