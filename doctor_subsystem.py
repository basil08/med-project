# builtins
import math
import time
import getpass
import random
import sys

# installed
from consolemenu import *
from consolemenu.items import *

# my modules
# import login
import doctor_view
import util
import db
import os

DOCTOR_INFO_TBL = os.getenv("DOCTOR_INFO_TBL")

def unauthorized_access():
    print('Unauthorized access: Incorrect Password')
    print('*'*20,' ABORT ','*'*20)

def new_signup():
    """ Self-explanatory
    Inserts a new valid record in the DOCTOR_INFO_TBL
    Checks uname is unique and verifies password by retyping
    """
    fname = input('Enter your first name: ').strip()
    lname = input('Enter your last name: ').strip()
    uname = input('Enter your username: ').strip()
    special = input('Enter your speciality: ').strip()
    assoc = input('Enter your organisation/association: ').strip()

    # ensure unique username
    while db.has(DOCTOR_INFO_TBL,'uname',uname):
        print('[-] Username taken: Try Again')
        uname = input('Enter your username: ')

    password = getpass.getpass(prompt='Create a strong password: ')
    retype_password = getpass.getpass(prompt='Retype password: ')
    
    if password != retype_password:
        print('Passwords do not match\nAbort')
        sys.exit()
    
    new_user = {'uname':uname, 'fname':fname, 'lname':lname, 'passwd':password, \
        'speciality': special, 'association': assoc, 'id': str(random.randint(1,100000))}

    if db.insert_record(DOCTOR_INFO_TBL, new_user):
        print(fname, lname, 'has been successfully added to the database')
    else:
        print('\nPLEASE TRY AGAIN')
    initialize()

def signup():
    util.cls()
    print('-----------')
    print('You did not enter a username and password during login\nDo you want to create an account?(y/N)')
    print('------------')
    ch = input()
    if ch in ['No','n','N','no']:
        print('Abort')
    elif ch in ['y','Y','yes','Yes']:
        new_signup()

def login():
    try:
        # clear current buffer
        util.cls()
        print("=========================")
        print("Welcome to doctor authentication portal")
        print("=========================")
        name = input('Username> ').strip()
        password = getpass.getpass(prompt='Password ??? ')
        
        if db.has(DOCTOR_INFO_TBL,'uname',name):
            # check for pass
            if not password == db.get_password(DOCTOR_INFO_TBL, name):
                unauthorized_access()
                sys.exit()
            else:
                print('Success: Authorization successful')
                return db.get_record_raw(DOCTOR_INFO_TBL, 'uname = "{}"'.format(name))
        else:
            print('Error: {0} does not exist in the database.'.format(name))
            print('Aborting login....')
        
        if name == '' and password == '':
            signup()
    except:
        pass            # for now

def show_submenu(menu):
    menu.show()

def initialize():
    record = login()
    if record == None: # shouldn't be needed, but a security check
        pass
    else:
        ## all the menus and submenus 
        menu = ConsoleMenu("Welcome, doctor {0}".format(record['fname']), "I am med, How can I help you today?")
        notifications_menu = ConsoleMenu("Notifications", "Send and receive notifs from your patients without hassle.")
        
        notifications_item = FunctionItem("Notifications", show_submenu, [notifications_menu])
        notifications_menu.append_item(FunctionItem("Read Recent Notifications", doctor_view.read_notifs, [record]))
        notifications_menu.append_item(FunctionItem("Send Notification", doctor_view.send_notifs, [record]))

        menu.append_item(notifications_item)
        time.sleep(1.5)
        menu.show()