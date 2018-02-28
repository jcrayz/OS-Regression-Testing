import allamericanregress
import sys
print('path:', sys.path)
print('__name__', __name__)

if __name__ == '__main__':
    try:
        allamericanregress.cli()
    except ModuleNotFoundError:
        print('script failed at runtime')
