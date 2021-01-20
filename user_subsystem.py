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
import user_view
import util
import db

# should ideally load from an environment variable 
# but ok for now
USER_INFO_TBL = 'user_info'

def unauthorized_access():
    print('Unauthorized access: Incorrect Password')
    print('*'*20,' ABORT ','*'*20)

def choose_doctor(tbl_name):
    try:
        doctors = db.get_list(tbl_name, 'fname')
        specialities = db.get_list(tbl_name, 'speciality')
        print('These doctors are available: ')
        for i in range(len(doctors)): print(i+1, doctors[i],'\t',specialities[i])
        ch = int(input("Enter a number: "))
        return doctors[ch-1]
    except:
        print("Error: Cannot retrieve available doctor froom doctor database")

def new_signup():
    """ Self-explanatory
    Inserts a new valid record in the USER_INFO_TBL
    Checks uname is unique and verifies password by retyping
    """
    fname = input('Enter your first name: ').strip()
    lname = input('Enter your last name: ').strip()
    uname = input('Enter your username: ').strip()
    email = input('Enter your email: ').strip()
    addr = input('Enter your address: (will be used in case of emergency) ').strip()
    phone = input('Enter your phone: (will be used in case of emergency) ').strip()
    doctor = choose_doctor('doctor_info')
    
    # ensure unique username
    while db.has(USER_INFO_TBL,'uname',uname):
        print('[-] Username taken: Try Again')
        uname = input('Enter your username: ')

    password = getpass.getpass(prompt='Create a strong password: ')
    retype_password = getpass.getpass(prompt='Retype password: ')
    
    if password != retype_password:
        print('Passwords do not match\nAbort')
        sys.exit()
    
    # TODO: can clash, future ver should ensure it is TRULY unique 
    new_user = {'uname':uname, 'fname':fname, 'lname':lname, 'passwd':password, 'id': str(random.randint(1,100000)), \
        'addr':addr,'phone':phone,'email':email, 'doctor': doctor}

    # write patients name to that doctor's dotfile
    # TODO: It seems except doesn't run if dotfile for doctor is not found
    # Maybe, i am having a wrong notion of the flow, thus investigate
    try:
        f = open('.{}_patients.txt'.format(doctor), 'a')
    except FileNotFoundError as err:
        print('Seems like no dotfile for {}'.format(doctor))
        print('Initializing one.....')
        f = open('.{}_patients.txt'.format(doctor), 'w')
        f.close()
    finally:   
        f.write(fname+' '+lname+'\n')
        f.close()

    if db.insert_record(USER_INFO_TBL, new_user):
        print(fname, lname, 'has been successfully added to the database')

        # Configure a defualt SOS message
        try:
            f = open('.{}_sos.txt'.format(fname), 'w')
            msg = 'HELP! HELP! HELP! I AM IN DANGER! PLEASE COME FAST.\n\n'
            f.write(msg)
            f.write('Patient name: {}\n'.format(fname+' '+lname))
            f.write('Address: {}\n'.format(addr))
            f.write('Phone: {}\n\n'.format(phone))
            f.close()
            print('Default SOS Configured: You can change your message with Config SOS')
            input("Press Enter to continue.....")
        except:
            pass
    else:
        print('\nPLEASE TRY AGAIN')
    initialize()


def signup():
    util.cls()
    print('-----------')
    # USE MENU HERE IN LINUX PLATFORMS
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
        print("Welcome to user authentication portal")
        print("=========================")
        name = input('Username> ').strip()
        password = getpass.getpass(prompt='Password:\n??? ')
        
        if db.has(USER_INFO_TBL,'uname',name):
            # check for pass
#            print('DEBUG: from user',password)
#            print('DEBUG: db',db.getPassword(USER_INFO_TBL, name))
            if not password == db.get_password(USER_INFO_TBL, name):
                unauthorized_access()
                sys.exit()
            else:
                print('Success: Authorization successful')
                return db.get_record_raw(USER_INFO_TBL, 'uname = "{}"'.format(name))
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
        # setup a menu
        # and welcome the patient

        ## all the menus and submenus 
        menu = ConsoleMenu("Welcome, {0}".format(record['fname']), "I am med, your personal health asistance program.")
        notifications_menu = ConsoleMenu("Notifications", "Be updated, be healthy. Always.")
        profile_menu = ConsoleMenu("View My Profile", "All your data, now at your fingertips.")



        export_bin_item = FunctionItem("Export Your Data To Binary", user_view.export_to_bin, [record])
        export_csv_item = FunctionItem("Export Your Data To CSV", user_view.export_to_csv, [record])
        basic_info_item = FunctionItem("View General Information", user_view.basic_info, [record])
        body_data_item = FunctionItem("View Body Data", user_view.body_data, [record])

        profile_item = FunctionItem("View My Profile", show_submenu, [profile_menu])


        # record_data_subitem = FunctionItem("Record Body Data", user_view.record_data, [record])

        # # NOTE: THIS record NOW HAS TO POINT TO THE NEW UPDATED RECORD OF THE PATIENT
        # # edit_data_subitem = FunctionItem("Edit Your Profile", user_view.edit_pfp, [record])

        appointment_menu = ConsoleMenu("Appointments", "Everything related to appointments in one place.")
        apppointment_item = FunctionItem("Appointments", show_submenu, [appointment_menu])
        appointment_menu.append_item(FunctionItem("Fix an Appointment", user_view.fix_appointment, [record]))
        appointment_menu.append_item(FunctionItem("My Appointments", user_view.read_appointments, [record]))

        notifications_item = FunctionItem("Notifications", show_submenu, [notifications_menu])
        notifications_menu.append_item(FunctionItem("Read Recent Notifications", user_view.read_notifs, [record]))
        notifications_menu.append_item(FunctionItem("Send Message", user_view.send_notifs, [record]))

        # sos_menu = ConsoleMenu("SOS Broadcast", "In case of emergency, we are always by your side.")
        # sos_item = FunctionItem("SOS Broadcast", show_submenu, [sos_menu])

        # medbay_menu = ConsoleMenu("Medbay Online", "One-stop shop for all your meds.")
        # medbay_item = FunctionItem("Medbay Online", show_submenu, [medbay_menu])

        # record_data_menu = ConsoleMenu("Record Your Data", "A dynamic history to better track your health.")
        # record_data_item = FunctionItem("Record Your Data", show_submenu, [record_data_menu])
        
        
        # edit_details_menu = ConsoleMenu("Edit Profile", "Edit your profile and preferences.")
        # edit_details_item = FunctionItem("Edit Profile", show_submenu, [edit_details_menu])
        # record_data_menu.append_item(record_data_subitem)

        profile_menu.append_item(body_data_item)
        profile_menu.append_item(export_csv_item)
        profile_menu.append_item(export_bin_item)
        profile_menu.append_item(basic_info_item)
        #edit_details_menu.append_item(edit_data_subitem)

        menu.append_item(notifications_item)
        menu.append_item(profile_item)
        menu.append_item(FunctionItem("Edit SOS Message", user_view.config_sos,[record]))
        menu.append_item(FunctionItem("Send SOS", user_view.broadcast_sos, [record]))
        menu.append_item(apppointment_item)
        # menu.append_item(medbay_item)
        # menu.append_item(record_data_item)
        # menu.append_item(user_view_details_item)
        #menu.append_item(edit_details_item)
        time.sleep(1.5)
        menu.show()

