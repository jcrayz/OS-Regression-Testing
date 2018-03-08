f = open('C:\\temp\\jennatest.log', 'a')
f.write('\nIn __main__.py')
f.close()

import allamericanregress

if __name__ == '__main__':
    try:
        print(f"Invoking cli from {__name__}")
        allamericanregress.cli()
    except ModuleNotFoundError:
        print('script failed at runtime')
