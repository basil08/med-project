import db
import time
import csv
import pickle
import datetime

# installed modules
import tabulate
import mysql

# my Errors
from myerr import NoSuchTableError


# a dummy moods list for now
moods = ['happy', 'sad', 'disappointed', 'depressed',
         'angry', 'excited', 'shocked', 'delighted']


def export_to_csv(record):
    """ Writes the contents of the table 'uname' where uname is supplied by the record to a CSV file in the same directory.
    returns: nothing
    reports success/failure to stdout
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
        db.init_tbl(record['uname'], ['timestamp datetime', 'weight dec(6,2)', 'height dec(6,2)',\
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
            # print('DEBUG: COUNT',db.count(tbl))
            for rcd in data:
                f.writerow(rcd)
            print('Success: Data written to {0}'.format(csvfilename))
        except:
            print("Error: Cannot write to {}".format(csvfilename))
        csvfile.close()
        input('Press Enter Key to Continue......')


def export_to_bin(record):
    """ Writes the contents of the table 'uname' where uname is supplied bu the record to a DAT file in the same directory.
    returns: nothing
    reports succss/failure to stdout
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
        db.init_tbl(record['uname'], ['timestamp datetime', 'weight dec(6,2)', 'height dec(6,2)',\
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
    """ puts basic info to stdout in tabular format
    basic info means data in 'user_info' tbl
    returns: nothing
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
    """ puts body data to stdout in tabular format
    body data is in a tbl for each user. 
    that table is read entirely.
    returns: nothing
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
        db.init_tbl(record['uname'], ['timestamp datetime', 'weight dec(6,2)', 'height dec(6,2)',\
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


def record_data(record):
    """ Update the record of a user with the data entered. Basically a INSERT mutation is run.
    Also handles the case of first time initialization.
    returns: bool (indicate success/failure)
    """
    tbl = record['uname'].strip()
    try:
        if not db.exists(tbl):
            raise NoSuchTableError()
    except NoSuchTableError:
        db.init_tbl(record['uname'], ['timestamp datetime', 'weight dec(6,2)', 'height dec(6,2)',\
                    'hrate dec(6,2)', 'pressure dec(6,2)', 'sleep int', 'steps int', 'mood varchar(14)'])
    finally:
        # continue with data entry anyway
        print(".....No external device detected.....")
        print(".....Reverting to manual data point entry.....")
        wt = float(input("Enter your weight: "))
        ht = float(input("Enter your height: "))
        hrate = float(input("Enter your heart rate: "))
        press = float(input("Enter your blood pressure: "))
        sleep = int(input("How many hours did you sleep last night?"))
        steps = int(input("How much did you walk yesterday?"))
        print(moods)

        # TODO: what if user entered something outside predefined moods
        mood = input("Choose one of the options above...")

        # wtf is this???!!
        mutation = 'insert into {0} values ("{1}",{2},{3},{4},{5},{6},{7},"{8}")'.format(
            tbl, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wt, ht, hrate, press, sleep, steps, mood)

        return db.insert_user_data(record, mutation)
#
# NOTIFICATION MODULE
#
# TODO: Allow users to see only 'unseen' notifications
# and give them choice to see as many as they want, eg: 5, 10, * (for all), etc


def read_notifs(record):
    try:
        f = open('.{}_notifs.txt'.format(record['fname']), 'r')
        print(f.read())
    except FileNotFoundError as err:
        print('Error: Notification hasn\'t been intialized for patient')
        # print(err.strerror)
        print('It seems like your doctor has nothing to say.')
    finally:
        input("Press Enter to continue....")


def send_notifs(record):
    """

    """
    try:
        doctor = record['doctor']
        print('Sending message to {}'.format(doctor))
        msg = input("Enter your message:\n")

        # open file stream
        try:
            f = open('.{}_notifs.txt'.format(doctor), 'a+')
            f.write('\n\n')
            f.write('Timestamp: ' + datetime.datetime.now().ctime() + '\n')
            f.write('Message: ' + msg + '\n')
            f.write('From: '+record['fname'])
            print('Success: Sent notification to {}'.format(doctor))
        except:
            pass
        finally:
            f.close()
    except:
        print('Error: Cannot send notification to {}'.format(doctor))
    finally:
        input("Press Enter to continue....")

#
# END NOTIFICATION MODULE
#


#
# SOS MODULE
#

def config_sos(record):
    """ Sets/Updates the Emergency SOS Broadcast message
    """
    try:
        f = open('.{}_sos.txt'.format(record['fname']), 'w')
        f.write(input('Enter your SOS Message: (Your phone and address are automatically broadcasted) '))
        f.write('\n\nPatient name: {}\n'.format(record['fname']+' '+record['lname']))
        f.write('Address: {}\n'.format(record['addr']))
        f.write('Phone: {}\n\n'.format(record['phone']))
        f.close()
        print("Success: Configured SOS Message for {}".format(record['fname']))
    except:
        pass        # for now

def broadcast_sos(record):
    """
    Email and notify _every_ doctor in the doctor database about this patient
    """
    try:
        # get the list of doctors from the database
        doctors = db.get_list('doctor_info', 'fname')

        # get the sos message from .<fname>_sos.txt
        f = open('.{}_sos.txt'.format(record['fname']), 'r')
        sos_msg = f.read()

        # open file stream
        # start looping over all doctors and write to their .notif files
        for doctor in doctors:
            try:
                f = open('.{}_notifs.txt'.format(doctor), 'a+')
                f.write('\n')
                f.write(sos_msg)
                f.write('Timestamp: ' + datetime.datetime.now().ctime() + '\n')
                # TODO: add email below
                #
                #
                print('Success: Sent SOS to {}'.format(doctor))
            except:
                pass
            finally:
                f.close()
    except:
        print('Error: Cannot send SOS to {}'.format(doctor))
    finally:
        input("Press Enter to continue....")
    

#
# END SOS MODULE
#
