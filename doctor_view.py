import datetime

from myerr import NoPatientError
import mail_service as ms
import db
import os

USER_INFO_TBL = os.getenv("USER_INFO_TBL")

def send_notifs(record):
    """
    read <doctor>_patients.txt file and ask who to send notification to...
    (If that file does not exist, exit with grace as noone has this doc assigned)
    Read the msg, write to <patient>_notifs.txt (create if doesn't exist)
    and try to send email to that id

    @param record {dict}
    @returns None
    """
    patients = get_patients(record)
    try:
        if len(patients) <= 0:
            raise NoPatientError
        for i in range(len(patients)): print(i+1, patients[i])
        # NOTE: patient is the fname of a patient, not the uname
        # -1 so as to normalize the effect of +1 abpve
        patient = patients[int(input("Who to send this notification? "))-1]
        raw_msg = input("Enter your message:\n")
        patient_email_id = db.get_list(USER_INFO_TBL, 'email', 'fname = "{}"'.format(patient))[0]
        # open file stream
        try:
            f = open('.{}_notifs.txt'.format(patient), 'w+')
            msg = '\n\n'
            msg += ('Timestamp: ' + datetime.datetime.now().ctime() + '\n')
            msg += ('Message: '+ raw_msg + '\n')
            msg += ('From: Dr. '+record['fname'])
            f.write(msg)
            # check if patient email id is not defined in database
            if patient_email_id != None:
                ms.send(patient_email_id, '{} | MED Notifications'.format(record['fname']), msg)
            else: print("Warning: Cannot send email notification.\nEmail id not defined in database.")
            print('Success: Sent notification to {}'.format(patient))
        except:
            print('Error: Cannot send notification to {}'.format(patient))
        finally:
            f.close()
    except:
        print('You are not assigned to any patient.\n')
    finally:
        input("Press Enter to continue....")

def get_patients(record):
    """
    read the doctors patients file and return a list of the patient's fname

    @param record {dict}
    @returns lst {list} list of patients this doctor is assigned to
    """
    lst = []
    try:
        f = open('.{}_patients.txt'.format(record['fname']), 'r')
        for line in f.readlines():
            lst.append(line.split()[0])
    except: pass
    finally: return lst

def read_notifs(record):
    """
    try to read this doctor's notifs.txt file.
    Handles non-existent file case.

    @param record {dict}
    @returns None
    """
    try:
        f = open('.{}_notifs.txt'.format(record['fname']), 'r')
        print(f.read())
    except FileNotFoundError as err:
        print('Error: Notification hasn\'t been intialized for doctor')
        # print(err.strerror)
        print('It seems like your patient has nothing to say.')
    finally: 
        input("Press Enter to continue....")
