"""AllAmericanRegress """
import argparse
import logging.config
import os
import subprocess
import sys

from . import config
from . import database_engine
from . import testing_framework
from . import utils
from . import webapp
from .service import AllAmericanRegressService


# configure logging to log everything to file and stdout
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(config.LOG_PATH)
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


ASADMIN = '--asadmin'

parser = argparse.ArgumentParser(
    description="Capstone regression testing program.")
# Register new program.
parser.add_argument(
    '--register',
    action='store_true',
    help="Flag to enable registering a new program.")
# Enable debug mode.
parser.add_argument(
    '--debug',
    action='store_true',
    help="Flag for enabling debug mode.")
# List all test results.
parser.add_argument(
    '--logs', action='store_true', help="Show all testing logs")
# Execute all tests.
parser.add_argument(
    '--execute-tests',
    action='store_true',
    help="Invoke the testing framework and log results.")
# Program path, only if registering.
parser.add_argument(
    '--path', metavar='path', help="Specify path of program to register.")
# Program name, only if registering.
parser.add_argument(
    '--name', metavar='name', help="Specify name for new registry entry.")
# Program command, only if registering.
parser.add_argument(
    '--command',
    metavar='command',
    help="""Specify command to execute the registry entry in the form 'command $1'. $1 will be replaced with the program path."""
)
# Program command, only if registering
parser.add_argument(
    '--author', metavar='author', help="Name of the author of the registry entry")
# List all programs.
parser.add_argument(
    '--list', action='store_true', help="List all registered applications.")
# Delete a program.
parser.add_argument(
    '--delete-id',
    type=int,
    metavar='delete_id',
    help="Option to delete entry by DB id.")
parser.add_argument(
    '--install-service',
    action='store_true',
    help="Install a Windows service to automatically execute tests after OS version updates.")
# Delete all config and DB files.
parser.add_argument(
    '--uninstall',
    action='store_true',
    help="Delete all config and logs for the application.")
# serve the webapp
parser.add_argument(
    '--webapp', action='store_true', help="Serve the Flask webapp.")
parser.add_argument(
    ASADMIN, action='store_true'
)
# Template to display when registering.
REGISTER_MESSAGE = """You are registering A program with the following details.
Name={}
Path={}
Command={}
"""


def cli():
    # detect number of cmd line args
    # fail early if no args found
    if len(sys.argv) == 1:
        # if none, print help and exit
        parser.print_help()
    if config.FROZEN:
        passed_args = sys.argv
    else:
        passed_args = sys.argv

    args = parser.parse_args()
    # print("Arguments:", args)

    if args.uninstall:
        utils.uninstall()

    if args.install_service:
        logger.info('Install service')
        if not config.FROZEN:
            install_proc = subprocess.Popen(['python', 'AllAmericanRegressService.py'], cwd=os.path.join(
                os.path.dirname(__file__), 'service'))
            logger.info(
                'Installing service from source dist. %s', install_proc)
            install_proc.wait()
            exit_code = install_proc.returncode
            if (exit_code == 0):
                print('Install succeeded.')
            else:
                print('There was an error installing.')
        else:
            logger.info(
                'Installing service from frozen dist.')
            AllAmericanRegressService.main()
            # install_proc = subprocess.Popen(
            #     ['regros.exe', '--install-frozen'], cwd=config.MODULE_PATH, shell=True)

    if args.delete_id:
        database_engine.deregister_program(args.delete_id)

    if args.list:
        for registrant in database_engine.all_registrants():
            print(registrant)

    if args.logs:
        print("ID, Name, Last Result, Version of Last Success, Date of Last Success")
        for i in database_engine.get_current_results():
            result = "Pass" if i[1].last_execution_id == i[1].last_successful_execution_id else "Fail"
            last_version = i[3].os_version if i[3] is not None else "None"
            last_success = i[3].pretty_time() if i[3] is not None else "Never"
            print("{}, {}, {}, {}, {}".format(i[0].id, i[0].name, result, last_version, last_success))

    if args.register:
        error = False
        # handle unsupplied path
        if args.path is None:
            print("Path must be supplied.")
            error = True
            path = None
        else:
            path = os.path.abspath(args.path)
            if not os.path.exists(path):
                print(
                    "Path {} does not exist! Please supply an existing path.".format(
                        repr(path)))
                error = True

        # handle unsupplied name
        if args.name is None:
            print("Name must be supplied.")
            error = True
        if args.command is None:
            print("Command must be supplied.")
            error = True
        if args.author is None:
            author = ''
        else:
            author = args.author
        if error:
            quit()
        print(REGISTER_MESSAGE.format(args.name, path, args.command))
        database_engine.register_program(args.name, path, args.command, author)

    if args.execute_tests:
        testing_framework.execute_tests()

    if args.webapp:
        logger.debug(f"Running webapp from command line via {__file__}")
        webapp.app.run(debug=args.debug)
