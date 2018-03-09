import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__,'..','..')))

import allamericanregress
if __name__ == '__main__':
    f = open('C:\\temp\\jennatest.log', 'a')
    f.write('\nIn __main__.py')
    f.close()
    try:
        print(f"Invoking cli from {__name__}")
        allamericanregress.cli()
    except ModuleNotFoundError:
        print('script failed at runtime')
