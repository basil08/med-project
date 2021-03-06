import mysql.connector as mc
import datetime
import time
import os

# Load the database secret from the env variable
DB_PASS = os.getenv('DB_PASS')

def init_db(host='localhost', user='Basil', passwd=DB_PASS, db='med1'):
    """
    Establish the database connection.

    @param host {string} host name
    @param user {string} user name
    @param passwd {string} the user password
    @param db {string} the database name

    @returns 2-tuple {SQLConnectionObject, SQLConnectionCursor}
    """
    try:
        mycon = mc.connect(host=host, user=user, password=passwd, database=db)
        cursor = mycon.cursor()
        print('.....Successfully established connection to database.....')
        return mycon, cursor
    except Error as e:
        print(e)

def desc_tbl(tbl_name):
    """
    Describe the table. A hacky debugging function.
    @param tbl_name {string} the table name
    @returns fetched data {dict}
    """
    cursor.execute('describe {0}'.format(tbl_name))
    return cursor.fetchall()

def snip(string, char=2):
    """ A tiny helper 
        should ideally be private but ok
    """
    return string[:len(string)-char]

def insert_record(tbl, data):
    """ Insert a PythonDict object ('data') into the tbl table
    data is a dictionary of user_info records. Think MongoDB in MySQL.
    NOTE: keys and values of the dict MUST be string.
    FUTURE TODO: allow lists as values and 'flatten' it into a string
    MySQL initializes unspecified fields with NULL 
    ONLY IF they are not declared as NOT NULL, in which case it throws an Error 
    TODO: Error handling doesn't show what is really wrong 

    @param tbl {string} the table name
    @param data {dict} the data to be inserted
    @returns bool (True if successful insertion, false otherwise)
    """
    try:
        flag = {}          # just a cheap hack and DONT be misled, its a dict inspite of its name
        # lst is basically a flag dictionary
        # it flags those fields which have 'varchar' in their definition (extracted by the typeof())
        # then if flag is 1 meaning the field in question is a varchar, enclose it in ""
        # else don't enclose in quotes
        mutation = 'insert into {} ('.format(tbl)
        for k in data.keys():
            mutation += (k+', ')
            if 'varchar' in typeof(tbl, k):
                flag[str(k)] = 1
            else:
                flag[k] = 0
        mutation = snip(mutation)
        mutation += ') values ('
        for k, v in data.items():
            if flag[k] == 1:
                mutation += ('"' + v + '" ,')
            else:
                mutation += (v + ', ')
        mutation = snip(mutation)
        mutation += ' );'
        cursor.execute(mutation)
        mycon.commit()
        return True
    except:
        print('[-] Error: Unable to add new entry to database.')
        return False

def typeof(tbl, field):
    """
    Returns the type of a field in a table.
    Calls desc_tbl

    @param tbl {string} table name
    @param field {string} the field whose type is to be known
    """
    schema = desc_tbl(tbl)
    for tpl in schema:
        if tpl[0] == field:
            return str(tpl[1])
    return None

def schema(tbl_name):
    """
    Returns a list of all the fieldnames in the table
    
    @param tbl_name {string} table name
    @returns {list} list of all fields
    """
    cursor.execute('describe {0}'.format(tbl_name))
    schema = cursor.fetchall()
    return [x for (x, _, _, _, _, _) in schema]

def exists(tbl_name):
    """
    Checks if tbl_name exists

    @param tbl_name {string} table name
    @returns {bool}
    """
    try:
        cursor.execute('desc {}'.format(tbl_name))
        data = cursor.fetchall()
        return True
    except mc.errors.DatabaseError:
        return False

def has(tbl, fieldname, val):
    """
    returns a bool for a simple exists or not condition on the field specified by the  first arg [fieldname] and value given by second arg [val].
    It simply checks for _at least_ one existence of that val in the tbl
    
    @param tbl_name {string} table name
    @param fieldname {string} field in tbl_name
    @param val {any} value to be searched for
    @return {bool}
    """
    mutation = 'select * from {0} where {1} = "{2}"'.format(
        tbl, fieldname, val)
    cursor.execute(mutation)
    return len(cursor.fetchall()) > 0

def count(tbl):
    """
    return a count of the number of records in the table tbl

    @param tbl {string} table name
    @returns {int} 0 if no records present
    """
    query = 'select count(*) from {0};'.format(tbl)
    cursor.execute(query)
    data = cursor.fetchall()[0]
    return int(data[0])

#
# GETTERS
# 
def get_list(tbl, field, condition=None):
    """
    return a python list of the form 'select field from tbl where condition'
    Default condition is None and if not passed is not considered in the query

    @param tbl {string}
    @param field {string}
    @param condition {string} Note: this MUST be a valid SQL query. If not given, is ignored.
    """
    try:
        query = 'select {} from {}'.format(field, tbl)
        if condition != None: query += ' where {}'.format(condition)
        query += ' ;'
        cursor.execute(query)
        data = cursor.fetchall()
        return [x[0] for x in data]
    except:
        print('Error: cannot read list from db in get_list')

def get_record(tbl, option):
    """
    returns a DictObject with the record matching option.key == options.value
    returns the first match, in case of multiple matched records, this is equivalent to get_records()[0]
    none if no results hit

    @param tbl {string}
    @param option {dict} option.key, option.value
    @returns {dict} first match
    """
    fieldname, val = option
    query = 'select * from {0} where {1} = "{2}"'.format(tbl, fieldname, val)
    cursor.execute(query)
    data = cursor.fetchone()
    return dict(zip(schema(tbl), data))

def get_record_raw(tbl, condition):
    """
    WARNING.
    Very Dangerous. Not recommended to use.
    Applies no filter on condition string. Simply executes it.

    @param tbl {string}
    @param condition {string} MUST be valid SQL string
    @return {dict} first match
    """
    query = 'select * from {} where {}'.format(tbl, condition)
    cursor.execute(query)
    data = cursor.fetchone()
    return dict(zip(schema(tbl), data))

def get_password(tbl, uname):
    """
    returns the password hash (builtin hash()) of the record whose uname is specified. 
    returns None if no such record exists in the table 'tbl'
    
    @param tbl {string}
    @param uname {string}
    @return {string} the password of uname
    """
    query = 'select passwd from {0} where uname = "{1}"'.format(tbl, uname)
    cursor.execute(query)
    data = cursor.fetchone()
    return data[0]

def get_all_raw(tbl):
    """
    pretty self-explanatory

    @param tbl {string}
    @returns {dict} everything unfiltered
    """
    query = 'select * from {0}'.format(tbl)
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def listify(data):
    """ Deprecated
    Flattens any high dimensional dataset into a 1d list of entries, suitable to add in a .CSV
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

def init_tbl(tbl_name, fields, primary=None):
    """
    python Interface around CREATE TABLE.
    fields [list] of string specifying name of field and their type as ['name varchar(10)', 'age int']
    if primary is not None, sets that field as PRI
    TODO: add NOT NULL, constraints and DEFAULT clause in a pretty way. (an obvious way is to include in 
    fields itself) 

    @param tbl_name {string}
    @param fields {list}
    @param primary {string} (optional)
    @returns None
    """
    try:
        mutation = 'create table {} ( '.format(tbl_name)
        for field in fields: mutation += field + ', '
        if primary != None: mutation += ' primary key({})'.format(primary)+', '
        mutation = snip(mutation)
        mutation += ' );'

        cursor.execute(mutation)
        mycon.commit()
        print("Success: Created new table {}".format(tbl_name))
    except mc.errors.ProgrammingError as err:
        print('Error: Could not create new table {}'.format(tbl_name))
        print(err.strerror)
    finally:
        input("Press Enter to continue......")

# Deprecated. 
# It's a function I am ashamed to have written in the first place.
# Don't use it!
def init_new_user_tbl(record):
    """ Make a new table in default database with the schema same for each patient and having tblname same as record['uname']
    returns: bool
    """
    try:
        # CHANGE HERE IF SCHEMA OF USER_DATA TBL CHANGES
        mutation = 'create table {0} ( timestamp datetime, weight dec(6,2), height dec(6,2), hrate dec(6,2), pressure dec(6,2), sleep int, steps int, mood varchar(14));'.format(
            record['uname'])
        cursor.execute(mutation)
        mycon.commit()
        print('Successfully created new table for patient {0}'.format(
            record['fname']+' '+record['lname']))
        return True
    except:
        print('Fatal Error: Could not create new table')

def insert_user_data(record, mutation):
    """
    WARNING: Executes raw string as SQL. NOT sanitized.
    records a specialised entry point for each user into their respective tables. 

    @param record {dict} the patient record
    @param mutation {string} MUST be valid SQL.
    @returns None
    """
    try:
        cursor.execute(mutation)
        mycon.commit()
        print('Data entry for patient {0} recorded successfully at {1}.'.format(
            record['fname']+' '+record['lname'], datetime.datetime.now()))
        input('Press Enter Key to Continue....')
        return True
    except:
        print('Error: Could not write data entry to your table.')

# let's roll
mycon, cursor = init_db()
