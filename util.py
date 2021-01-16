import os
import time

def cls(delay=1.0):
    """
        wait for sometime for user to absorb info on screen (so that not abrupt flush)
        recognize the platform using os.name 
        and accordingly execute clearing using a system call
        delay [float]: number of seconds to wait
        returns: nothing
    """
    time.sleep(delay)
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print('WARNING: Unsupported platform detected.\nSome features may not work as intended.')


