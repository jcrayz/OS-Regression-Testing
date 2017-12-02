from allamericanregress import database_engine
import subprocess
import logging
logger = logging.getLogger(__name__)


def main():
    for p in database_engine.all_entries():
        command = p[-1].replace('$1', p[2])
        child = subprocess.Popen(command.split(' '))
        child.communicate()
        code = child.returncode
        if code != 0:
            logger.log(logging.DEBUG, "Test {} failed.".format(p))
        print("Test {} exited with code {}".format(p, code))


if __name__ == '__main__':
    main()
