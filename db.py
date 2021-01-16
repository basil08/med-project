import mysql.connector as mc
import datetime
import time

#
# TODO: Use environment variable to store passwd ffs 
#

def init_db(host='localhost', user='Basil', passwd='2a19i12',db='med1'):
    try:
        mycon = mc.connect(host=host, user=user, password=passwd, database=db)
        cursor = mycon.cursor()
        print('.....Successfully established connection to database.....')
        return mycon, cursor
    except Error as e:
        print(e)

def desc_tbl(tbl_name):
    cursor.execute('describe {0}'.format(tbl_name))
    return cursor.fetchall()
    # schema is a list on n tuples with n field names and meta
    # so get just the first of those (the name)

def snip(string, char=2):
    return string[:len(string)-char]

def insert_record(tbl, data):
    """ Insert a PythonDict object ('data') into the tbl table
    
    data is a dictionary of user_info records. Think MongoDB in MySQL.

    NOTE: keys and values of the dict MUST be string.
    
    FUTURE TODO: allow lists as values and 'flatten' it into a string

    returns: bool (True if successfull insertion, false otherwise)
    """
    try:
        lst = {}          # just a cheap hack and DONT be misled, its a dict inspite of its name
        # lst is basically a flag dictionary
        # it flags those fields which have 'varchar' in their definition (extracted by the typeof())
        # then if flag is 1 meaning the field in question is a varchar, enclose it in ""
        # else don't enclose in quotes
        mutation = 'insert into {} ('.format(tbl)
        for k in data.keys():  
            mutation += (k+', ')
            if 'varchar' in typeof(tbl, k): lst[str(k)] = 1
            else: lst[k] = 0
        mutation = snip(mutation)
        mutation += ') values ('
        for k, v in data.items():
            if lst[k] == 1: mutation += ('"' + v + '" ,') 
            else: mutation += (v + ', ')
        mutation = snip(mutation)
        mutation += ' );'
        print('DEBUG final insert record string: ',mutation)
        cursor.execute(mutation)
        mycon.commit()
        return True
    except:
        print('[-] Error: Unable to add new entry to database.')
        return False
    

def typeof(tbl, field):
    schema = desc_tbl(tbl)
    for tpl in schema: 
        if tpl[0] == field: return str(tpl[1])
    return None
    
def schema(tbl_name):
    """ Returns a list of all the fieldnames in the table
    """
    cursor.execute('describe {0}'.format(tbl_name))
    schema = cursor.fetchall()
    return [x for (x,_,_,_,_,_) in schema]

def has(tbl, fieldname, val):
    """ This function returns a bool for a simple exists or not condition on the field specified by the  first arg [fieldname] and value given by second arg [val].

    It simply checks for _at least_ one existence of that val in the tbl

    returns: bool
    """

    mutation = 'select * from {0} where {1} = "{2}"'.format(tbl, fieldname, val)
#    print('DEBUG:',mutation)
   
    cursor.execute(mutation)
    return len(cursor.fetchall()) > 0

def count(tbl):
    """ Return a count of the number of records in the table tbl
    returns: int
    0 if no records present
    """
    query = 'select count(*) from {0};'.format(tbl)
    cursor.execute(query)
    data = cursor.fetchall()[0]
    #print('DEBUG count:',data)
    return int(data[0])

def getAll(tbl):
    """ Pretty self-explanatory
    """

    query = 'select * from {0}'.format(tbl)
    cursor.execute(query)
    data = cursor.fetchall()
    return data
    # TODO:convert datetime.datetime to a string representation (see man)
    # TODO: convert Decimal('12.33') to float (idk yet)
    


def listify(data):
    """ Flattens any high dimensional dataset into a 1d list of entries, suitable to add in a .CSV
    WARNING: IMPORTANT CAVEAT. THIS IS NOT  A GENERAL FUNCTION. It works only by assuming the schema of the user tbl
    NB: rcd = record
    """
    lst = []
    for rcd in data:
        rcd_lst = []
        rcd_lst.append(datetime.datetime.ctime(rcd[0]))
        rcd_lst.append(float(rcd[1]))
        rcd_lst.append(float(rcd[2]))
        rcd_lst.append(float(rcd[3]))
        rcd_lst.append(float(rcd[4]))
        rcd_lst.append(int(rcd[5]))
        rcd_lst.append(int(rcd[6]))
        rcd_lst.append(str(rcd[7]))
        lst.append(rcd_lst)
    return lst

# Deprecated. It's a function I am ashamed to have written in the first place. Don't use it!
def init_new_user_tbl(record):
    """ Make a new table in default database with the schema same for each patient and having tblname same as record['uname']
    returns: bool
    """
    try:
        ## CHANGE HERE IF SCHEMA OF USER_DATA TBL CHANGES
        mutation = 'create table {0} ( timestamp datetime, weight dec(6,2), height dec(6,2), hrate dec(6,2), pressure dec(6,2), sleep int, steps int, mood varchar(14));'.format(record['uname'])
        cursor.execute(mutation)
        mycon.commit()
        print('Successfully created new table for patient {0}'.format(record['fname']+' '+record['lname']))
        return True
    except:
        print('Fatal Error: Could not create new table')

def snip(string, char=2):
    return string[:len(string)-char]


def insert_record(tbl, data):
    """ Insert a PythonDict object ('data') into the tbl table
    
    data is a dictionary of user_info records. Think MongoDB in MySQL.

    returns: bool (True if successfull insertion, false otherwise)
    """
    try:
        mutation = 'insert into {} ('.format(tbl)
        for k in data.keys():  
            mutation += (k+', ')
        print('before snip', mutation)
        mutation = snip(mutation)
        print('after snip', mutation)
        mutation += ') values ('
        for v in data.values():
            mutation += (v + ', ')
        mutation = snip(mutation)
        mutation += ' );'
        print('DEBUG final insert record string: ',mutation)
        cursor.execute(mutation)
        mycon.commit()
        return True
    except:
        print('[-] Error: Unable to add new entry to database.')
        return False

def insert_user_data(record, mutation):
    """ Records a specialised entry point for each user into their respective tables. 
    returns: bool
    """
    try:
        cursor.execute(mutation)
        mycon.commit()
        print('Data entry for patient {0} recorded successfully at {1}.'.format(record['fname']+' '+record['lname'], datetime.datetime.now()))
        input('Press Enter Key to Continue....')
        return True
    except: 
        print('Error: Could not write data entry to your table.')


#
# This thing is not working properly
def get_records(tbl, fieldname, val):
    """ Returns a Python DictObject with the record having fieldname = val
    
    returns: a list of _all_ matched records
    """
    query = 'select * from {0} where {1} = "{2}"'.format(tbl, fieldname, val)
    cursor.execute(query)
    data = cursor.fetchall()

    return data

# And this thing also...
def get_record(tbl, fieldname, val):
    """ Returns a DictObject with the record hacing fieldname = val

    returns: the first match, in case of multiple matched records, this is equivalent to get_records()[0]
    none if no results hit
    """
    query = 'select * from {0} where {1} = "{2}"'.format(tbl, fieldname, val)
    cursor.execute(query)
    data = cursor.fetchone()

    return dict(zip(schema(tbl), data))

def get_password(tbl, uname):
    """ Returns the password hash (builtin hash()) of the record whose uname is specified. 
    returns None if no such record exists in the table 'tbl'
    """
    query = 'select passwd from {0} where uname = "{1}"'.format(tbl, uname)
#    print('DEBUG:',query)
    cursor.execute(query)
    data = cursor.fetchone()
    return data[0]

def exec(mutation):

    # add pre-processing here 
    cursor = connect()

    cursor.execute(mutation)
    
    data = cursor.fetchall()

mycon, cursor = init_db()
