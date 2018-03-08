import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__,'..','..')))

import allamericanregress
if __name__ == '__main__':
    try:
        allamericanregress.cli()
    except ModuleNotFoundError:
        print('script failed at runtime')
