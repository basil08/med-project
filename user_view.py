from myerr import NoSuchTableError, NoPatientError
import db
import time
import csv
import pickle
import datetime

# installed modules
import tabulate
import mysql

# my modules
import mail_service as ms
import os

DOCTOR_INFO_TBL = os.getenv('DOCTOR_INFO_TBL')

# a dummy moods list for now
moods = ['happy', 'sad', 'disappointed', 'depressed',
         'angry', 'excited', 'shocked', 'delighted']

def export_to_csv(record):
    """
    writes the contents of the table 'uname' where uname is supplied by the record to a CSV file in the same directory.
    reports success/failure to stdout

    @param record {dict} the patient record
    @return None
    """
    csvfilename = record['fname']+'_'+record['lname']+'.csv'
    try:
        # write the headers
        # the username is the name of the table
        if not db.exists(record['uname']):
            raise NoSuchTableError()
    except NoSuchTableError:
        print("Error: No table for {} exists in database.".format(
            record['fname']))
        print("Creating new table for {}".format(record['fname']))
        db.init_tbl(record['uname'], ['timestamp datetime', 'weight dec(6,2)', 'height dec(6,2)',
                                      'hrate dec(6,2)', 'pressure dec(6,2)', 'sleep int', 'steps int', 'mood varchar(14)'])
        print("Created new table for {}".format(record['uname']))
    # attempt writing to csv after confirming table exists to read from
    # if doesn't, then init new empty table
    finally:
        csvfile = open(csvfilename, 'w', newline='')
        f = csv.writer(csvfile)
        tbl = record['uname'].strip()
        headers = db.schema(tbl)
        f.writerow(headers)
        try:
            # listify() flattens everything into a 1d list of entries
            data = db.listify(db.get_all_raw(tbl))
            for rcd in data:
                f.writerow(rcd)
            print('Success: Data written to {0}'.format(csvfilename))
        except:
            print("Error: Cannot write to {}".format(csvfilename))
        csvfile.close()
        input('Press Enter Key to Continue......')

def export_to_bin(record):
    """
    writes the contents of the table 'uname' where uname is supplied bu the record to a DAT file in the same directory.
    reports succss/failure to stdout

    @param record {dict}
    @returns None
    """
    try:
        # write the headers
        # the username is the name of the table
        if not db.exists(record['uname']):
            raise NoSuchTableError()
    except NoSuchTableError:
        print("Error: No table for {} exists in database.".format(
            record['fname']))
        print("Creating new table for {}".format(record['fname']))
        db.init_tbl(record['uname'], ['timestamp datetime', 'weight dec(6,2)', 'height dec(6,2)',
                                      'hrate dec(6,2)', 'pressure dec(6,2)', 'sleep int', 'steps int', 'mood varchar(14)'])
        print("Created new table for {}".format(record['uname']))
    finally:
        datfilename = record['fname']+'_'+record['lname']+'.dat'
        datfile = open(datfilename, 'wb')

        # seggragate the table name and dump schema headers into dat file
        tbl = record['uname'].strip()
        headers = db.schema(tbl)
        pickle.dump(headers, datfile)

        data = db.listify(db.get_all_raw(tbl))
        pickle.dump(data, datfile)

        print('Success: Data written to {0}'.format(datfilename))
        datfile.close()
        input('Press Enter Key to Continue.........')

def basic_info(record):
    """
    puts basic info to stdout in tabular format
    basic info means data in 'user_info' tbl

    @param record {dict}
    @returns None
    """
    print("---------------------------")
    print("GENERAL INFORMATION FOR ", record['fname'], record['lname'])
    print("---------------------------")

    l = [[k, record[k]] for k in record]

    # obscure password for security
    l[3][1] = '*************'

    print(tabulate.tabulate(l, headers=["Field", "Data"], tablefmt="pretty"))
    input('Return to continue.....')

def body_data(record):
    """
    puts body data to stdout in tabular format
    body data is in a tbl for each user. 
    that table is read entirely.

    @param record {dict}
    @returns None
    """
    try:
        # write the headers
        # the username is the name of the table
        if not db.exists(record['uname']):
            raise NoSuchTableError()
    except NoSuchTableError:
        print("Error: No table for {} exists in database.".format(
            record['fname']))
        print("Creating new table for {}".format(record['fname']))
        db.init_tbl(record['uname'], ['timestamp datetime', 'weight dec(6,2)', 'height dec(6,2)',
                                      'hrate dec(6,2)', 'pressure dec(6,2)', 'sleep int', 'steps int', 'mood varchar(14)'])
        print("Created new table for {}".format(record['uname']))
    finally:
        print('-'*50)
        print("DATA REPOSITORY FOR", record['fname'], record['lname'])
        print('-'*50)
        tbl = record['uname'].strip()
        # TODO: what if uname does not exist?
        data = db.listify(db.get_all_raw(tbl))
        print(tabulate.tabulate(data, headers=db.schema(tbl), tablefmt="pretty"))
        input("Press Return Key to Continue......")

        return db.insert_user_data(record, mutation)

#
# NOTIFICATION MODULE
#
def read_notifs(record):
    """
    Straight-forward, try to open the user's notifs text file and read all notifications.
    If File doesn't exist, then doctor assigned has not notified even once.
    Delete the <uname>_notifs.txt file to reset notifs for this user.

    @param record {dict}
    @returns None
    """
    try:
        f = open('.{}_notifs.txt'.format(record['fname']), 'r')
        print(f.read())
    except FileNotFoundError as err:
        print('Error: Notification hasn\'t been intialized for patient')
        print('It seems like your doctor has nothing to say.')
    finally:
        input("Press Enter to continue....")

def send_notifs(record):
    """
    Get this patients doctor record from db, then fetch that doctors email.
    Input msg and try to send an email and write to <doctor>_notifs.txt
    Handle exceptions related to email here

    @param record {dict}
    @returns None
    """
    try:
        doctor = record['doctor']
        print('Sending message to {}'.format(doctor))
        raw_msg = input("Enter your message:\n")
        # query email id of doctor from db
        # as get_list returns a list, add a condition and fetch only the first email id
        doctor_email_id = db.get_list(
            DOCTOR_INFO_TBL, 'email', 'fname = "{}"'.format(doctor))[0]
        # open file stream
        try:
            f = open('.{}_notifs.txt'.format(doctor), 'a+')
            msg = '\n\n'
            msg += ('Timestamp: ' + datetime.datetime.now().ctime() + '\n')
            msg += ('Message: ' + raw_msg + '\n')
            msg += ('From: '+record['fname'])
            f.write(msg)

            # check if email id of doctor is not in database
            if doctor_email_id != None:
                ms.send(doctor_email_id, '{} | MED notifications'.format(
                    record['fname']), msg)
            else:
                print(
                    "Warning: Cannot send email notification.\nEmail id not defined in database.")
            print('Success: Sent notification to {}'.format(doctor))
        except:
            print("Error: Could not send email notification to {}".format(doctor))
        finally:
            f.close()
    except:
        print('Error: Cannot send notification to {}'.format(doctor))
    finally:
        input("Press Enter to continue....")
# END NOTIFICATION MODULE

# SOS MODULE
#
def config_sos(record):
    """
    sets/updates the Emergency SOS Broadcast message

    @param record {dict}
    @returns None
    """
    try:
        f = open('.{}_sos.txt'.format(record['fname']), 'w')
        f.write(input(
            'Enter your SOS Message: (Your phone and address are automatically broadcasted) '))
        f.write('\n\nPatient name: {}\n'.format(
            record['fname']+' '+record['lname']))
        f.write('Address: {}\n'.format(record['addr']))
        f.write('Phone: {}\n\n'.format(record['phone']))
        f.close()
        print("Success: Configured SOS Message for {}".format(record['fname']))
    except:
        pass        # for now
    finally:
        input("Press Enter to continue....")

def broadcast_sos(record):
    """
    email and notify _every_ doctor in the doctor database about this patient
    
    @param record {string}
    @returns None
    """
    try:
        # get the list of doctors from the database
        doctors = db.get_list(DOCTOR_INFO_TBL, 'fname')

        mail_ids = db.get_list(DOCTOR_INFO_TBL, 'email')

        # get the sos message from .<fname>_sos.txt
        f = open('.{}_sos.txt'.format(record['fname']), 'r')
        sos_msg = f.read()

        # open file stream
        # start looping over all doctors and write to their .notif files
        for doctor, mail_id in zip(doctors, mail_ids):
            try:
                # 'a+' as the file may not already exist
                f = open('.{}_notifs.txt'.format(doctor), 'a+')
                msg = '\n'
                msg += sos_msg
                msg += 'Timestamp: ' + datetime.datetime.now().ctime() + '\n'
                f.write(msg)
                # TODO: add email below
                ms.send(mail_id, 'HELP! I AM IN DANGER!', msg)
                #
                print('Success: Sent SOS to {}'.format(doctor))
            except:
                pass
            finally:
                f.close()
    except:
        print('Error: Cannot send SOS to {}'.format(doctors))
    finally:
        input("Press Enter to continue....")
#
# END SOS MODULE
#
