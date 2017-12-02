import argparse

parser = argparse.ArgumentParser(
    description="Capstone regression testing program.")
parser.add_argument('--register', action='store_true',
                    help="Flag to enable registering a new program.")
parser.add_argument('--path', metavar='path',
                    help="Specify path of program to register.")
parser.add_argument('--name', metavar='name',
                    help="Specify nam for new registry entry.")


def main():
    args = parser.parse_args()
    print("Arguments:", args)
    if args.register:
        print("""You are registering A program with the following details.
Path={}
Name={}""".format(args.path, args.name))


if __name__ == '__main__':
    main()
