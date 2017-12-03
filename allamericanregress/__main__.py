import sys
import argparse
import os
from allamericanregress import config
from allamericanregress import database_engine
from allamericanregress import utils
from allamericanregress import testing_framework
import logging
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="Capstone regression testing program.")
parser.add_argument('--register', action='store_true',
                    help="Flag to enable registering a new program.")
parser.add_argument('--logs', action='store_true',
                    help="Show all testing logs")
parser.add_argument('--execute-tests', action='store_true',
                    help="Invoke the testing framework and log results.")
parser.add_argument('--path', metavar='path',
                    help="Specify path of program to register.")
parser.add_argument('--name', metavar='name',
                    help="Specify name for new registry entry.")
parser.add_argument('--command', metavar='command',
                    help="""Specify command to execute the registry entry in the form 'command $1'. $1 will be replaced with the program path.""")
parser.add_argument('--list', action='store_true',
                    help="List all registered applications.")
parser.add_argument('--delete-id', type=int, metavar='delete_id',
                    help="Option to delete entry by DB id.")
parser.add_argument('--uninstall', action='store_true',
                    help="Delete all config and logs for the application.")
REGISTER_MESSAGE = """You are registering A program with the following details.
Name={}
Path={}
Command={}
"""


def main():
    # detect number of cmd line args
    # fail early if no args found
    if len(sys.argv) == 1:
        # if none, print help and exit
        parser.print_help()
        quit()

    args = parser.parse_args()
    # print("Arguments:", args)

    if args.uninstall:
        print("Uninstalling...")
        utils.uninstall()

    if args.delete_id:
        database_engine.deregister_program(args.delete_id)
    if args.list:
        for i in database_engine.all_entries():
            print(i)
    if args.logs:
        for i in database_engine.all_test_logs():
            print(i)

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
                    "Path {} does not exist! Please an existing path.".format(repr(path)))
                error = True

        # handle unsupplied name
        if args.name is None:
            print("Name must be supplied.")
            error = True
        if args.command is None:
            print("Command must be supplied.")
            error = True
        if error:
            quit()
        print(REGISTER_MESSAGE.format(args.name, path, args.command))
        database_engine.register_program(args.name, path, args.command)

    if args.execute_tests:
        testing_framework.execute_tests()

if __name__ == '__main__':
    main()
