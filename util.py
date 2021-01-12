import os

def cls():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print('WARNING: Unsupported platform detected.\nSome features may not work as intended.')


