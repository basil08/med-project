import datetime

def send_notifs(record):
    """

    """
    patients = get_patients(record)
    try:
        if len(patients) <= 0:
            print('You are not assigned to any patient.\n')
            # TODO: Write a Error as NoPatientError
            # and change the below line ffs
            # raise NoFileFoundError
            # remove if/else when NoPatientError is implemented
        else:    
            # i+1 as improved UX. indexing from 1...
            for i in range(len(patients)): print(i+1, patients[i])
            # NOTE: patient is the fname of a patient, not the uname
            # -1 so as to normalize the effect of +1 abpve
            patient = patients[int(input("Who to send this notification? "))-1]
            msg = input("Enter your message:\n")

            # open file stream
            try:
                f = open('.{}_notifs.txt'.format(patient), 'a+')
                f.write('\n\n')
                f.write('Timestamp: ' + datetime.datetime.now().ctime() + '\n')
                f.write('Message: '+ msg + '\n')
                f.write('From: Dr. '+record['fname'])
                print('Success: Sent notification to {}'.format(patient))
            except:
                print('Error: Cannot send notification to {}'.format(patient))
            finally:
                f.close()
    except:
        pass
    finally:
        input("Press Enter to continue....")


def get_patients(record):
    """
    Read the doctors patients file and return a list of the patient's fname
    
    """
    lst = []
    try:
        f = open('.{}_patients.txt'.format(record['fname']), 'r')
        for line in f.readlines():
            lst.append(line.split()[0])
    except: pass
    finally: return lst

def read_notifs(record):
    try:
        f = open('.{}_notifs.txt'.format(record['fname']), 'r')
        print(f.read())
    except FileNotFoundError as err:
        print('Error: Notification hasn\'t been intialized for doctor')
        # print(err.strerror)
        print('It seems like your patient has nothing to say.')
    finally: 
        input("Press Enter to continue....")
