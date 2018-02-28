import allamericanregress

if __name__ == '__main__':
    try:
        allamericanregress.cli()
    except ModuleNotFoundError:
        print('script failed at runtime')
