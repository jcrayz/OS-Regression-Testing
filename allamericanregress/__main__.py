import allamericanregress
import os
import sys
# add the modiule location to PATH
# this is necessary to execute the package as a script without installing it
to_append = os.path.dirname(os.path.dirname(__file__))
sys.path.append(to_append)

if __name__ == '__main__':
    try:
        print(f"Invoking cli from {__name__}")
        allamericanregress.cli()
    except ModuleNotFoundError:
        print('script failed at runtime')
