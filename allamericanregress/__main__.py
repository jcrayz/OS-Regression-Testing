import os
import sys

# add the module location to PATH
# this is necessary to execute the package as a script without installing it
# TODO: Use Frozen path
to_append = os.path.dirname(os.path.dirname(__file__))
sys.path.append(to_append)

import allamericanregress
if __name__ == '__main__':
    try:
        allamericanregress.cli()
    except ModuleNotFoundError:
        print('script failed at runtime')
