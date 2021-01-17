import db
import time
import csv
import pickle
import datetime

# installed modules
import tabulate


# a dummy moods list for now
moods = ['happy','sad','disappointed','depressed','angry','excited','shocked','delighted']

def export_to_csv(record):
    """ Writes the contents of the table 'uname' where uname is supplied by the record to a CSV file in the same directory.
    returns: nothing
    reports success/failure to stdout
    """
    csvfilename = record['fname']+'_'+record['lname']+'.csv'
    csvfile = open(csvfilename, 'w', newline='')

    f = csv.writer(csvfile)
    # write the headers
    # the username is the name of the table
    tbl = record['uname'].strip()
    headers = db.schema(tbl)
    f.writerow(headers)
     
    # listify() flattens everything into a 1d list of entries
    data = db.listify(db.getAll(tbl))
    #print('DEBUG: COUNT',db.count(tbl))
    for rcd in data:
        f.writerow(rcd)
    print('Success: Data written to {0}'.format(csvfilename))
    input('Press Enter Key to Continue......')
    csvfile.close()

def export_to_bin(record):
    """ Writes the contents of the table 'uname' where uname is supplied bu the record to a DAT file in the same directory.
    returns: nothing
    reports succss/failure to stdout
    """
    datfilename = record['fname']+'_'+record['lname']+'.dat'
    datfile = open(datfilename, 'wb')

    # seggragate the table name and dump schema headers into dat file
    tbl = record['uname'].strip()
    headers = db.schema(tbl)
    pickle.dump(headers, datfile)

    data = db.listify(db.getAll(tbl))
    pickle.dump(data, datfile)

    print('Success: Data written to {0}'.format(datfilename))
    input('Press Enter Key to Continue.........')
    datfile.close()

def basic_info(record):
    """ puts basic info to stdout in tabular format
    basic info means data in 'user_info' tbl
    returns: nothing
    """
    print("---------------------------")
    print("GENERAL INFORMATION FOR ", record['fname'], record['lname'])
    print("---------------------------")

    l=[[k,record[k]] for k in record]

    # obscure password for security
    l[3][1] = '*************'

    print(tabulate.tabulate(l, headers=["Field","Data"], tablefmt="pretty"))
    input('Return to continue.....')

def body_data(record):
    """ puts body data to stdout in tabular format
    body data is in a tbl for each user. 
    that table is read entirely.
    returns: nothing
    """
    print('-'*50)
    print("DATA REPOSITORY FOR",record['fname'],record['lname'])
    print('-'*50)
    
    tbl = record['uname'].strip()

    # TODO: what if uname does not exist?
    data = db.listify(db.getAll(tbl))
    print(tabulate.tabulate(data, headers=db.schema(tbl), tablefmt="pretty"))
    input("Press Return Key to Continue......")

def record_data(record):
    """ Update the record of a user with the data entered. Basically a INSERT mutation is run.
    Also handles the case of first time initialization.
    returns: bool (indicate success/failure)
    """
    tbl = record['uname'].strip()
    try:
        db.exec('select * from {0}'.format(record['uname']))
    except:
        # if tbl uname does not exist
        db.init_new_user_tbl(record)
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

        mutation = 'insert into {0} values ("{1}",{2},{3},{4},{5},{6},{7},"{8}")'.format(tbl, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wt, ht, hrate, press, sleep, steps, mood)
        
        return db.insert_user_data(record, mutation)

def read_notifs(record):
    try:
        f = open('.{}_notifs.txt'.format(record['uname']), 'r')
        print(f.read())
    except FileNotFoundError as err:
        print('Error: Notification hasn\'t been intialized for patient')
        # print(err.strerror)
        print('It seems like your doctor has nothing to say.')
    finally: 
        input("Press Enter to continue....")





