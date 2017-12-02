import sys
import argparse
import os
from allamericanregress import config
from allamericanregress import database_engine
import logging
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="Capstone regression testing program.")
parser.add_argument('--register', action='store_true',
                    help="Flag to enable registering a new program.")
parser.add_argument('--path', metavar='path',
                    help="Specify path of program to register.")
parser.add_argument('--name', metavar='name',
                    help="Specify nam for new registry entry.")
parser.add_argument('--list', action='store_true',
                    help="List all registered applications.")
REGISTER_MESSAGE = """You are registering A program with the following details.
Name={}
Path={}
"""


def main():
    error = False
    # detect number of cmd line args
    # fail early if no args found
    if len(sys.argv) == 1:
        # if none, print help and exit
        parser.print_help()
        quit()

    args = parser.parse_args()
    # print("Arguments:", args)

    if args.list:
        cursor = database_engine.database_connection.cursor()
        for i in cursor.execute("SELECT * FROM programs"):
            print(i)
        quit()
        # handle unsupplied path
    if args.path is None:
        print("Path (--path) must be supplied.")
        error = True
        path = None
    else:
        path = os.path.abspath(args.path)

    # handle unsupplied name
    if args.name is None:
        print("Name (--name) must be supplied.")
        error = True

    if error:
        quit()

    if args.register:
        print(REGISTER_MESSAGE.format(args.name, path))
        database_engine.register_program(args.name, path)


if __name__ == '__main__':
    main()
