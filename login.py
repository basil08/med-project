import getpass
import sys
import random

import db
import util

""" known bugs:

    the else runs _after_ code inside if has run. Happens only when signup() is called (with success) and user tries their first login.
    status: severe issue
    result: program aborts
"""



def unauthorized_access():
    print('Unauthorized access: Incorrect Password')
    print('_'*20,' ABORT ','_'*20)

def login():
    try:
        name = input('Username> ').strip()
        password = getpass.getpass(prompt='Password ??? ')
        
        if name == '' and password == '':
            signup()

#        if ch == 'a': tbl_name = 'admin_info'
#       elif ch == 'u': tbl_name = 'user_info'

        if db.has('user_info','uname',name):
            # check for pass
#            print('DEBUG: from user',password)
#            print('DEBUG: db',db.getPassword('user_info', name))
            if not password == db.get_password('user_info', name):

                unauthorized_access()
                sys.exit()
            else:

                print('Success: Authorization successful')
                return db.get_record_one('user_info','uname',name)
        else:
            print('Error: {0} does not exist in the database.'.format(name))
            print('Abort')
            sys.exit()
    except:
        pass            # for now

def signup():
    util.cls()
    print('-----------')
    
    #
    # USE MENU HERE IN LINUX PLATFORMS
    #
    print('You did not enter a username and password during login\nDo you want to create an account?(y/N)')
    
    print('------------')
    ch = input()
    if ch in ['No','n','N','no']:
        print('Abort')
    elif ch in ['y','Y','yes','Yes']:
        new_signup()

def new_signup():
    fname = input('Enter your first name: ').strip()
    lname = input('Enter your last name: ').strip()
    uname = input('Enter your username: ').strip()
    
    # ensure unique username
    while db.has('user_info','uname',uname):
        print('[-] Username taken: Try Again')
        uname = input('Enter your username: ')

    password = getpass.getpass(prompt='Create a strong password: ')
    retype_password = getpass.getpass(prompt='Retype password: ')
    
    if password != retype_password:
        print('Passwords do not match\nAbort')
        sys.exit()
    

    new_user = {'uname':uname, 'fname':fname, 'lname':lname, 'passwd':password, 'id': random.randint(1,100000)} # TODO: can clash, future ver should ensure it is TRULY unique

    if db.insert_one_user('user_info', new_user):
        print(fname, lname, 'has been successfully added to the database')
    else:
        print('\nPLEASE TRY AGAIN')
    login()

    
