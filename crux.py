import mysql.connector as mc
import config

USERNAME = config.USERNAME
PASS = config.PASSWORD
DBNAME = config.DBNAME

def getDbConnection():
    # connecting to DB
    try:
        print("...Connecting to DB...")
        cnx = mc.connect(user=USERNAME,
                        passwd=PASS,
                        host='localhost',
                        database=DBNAME)

        print("...Connection Sucessful...")
        cursor = cnx.cursor()
        return cursor, cnx
    except mc.Error as err:
        print("Something went wrong in Connecting to DB: {}".format(err))

def insertDb(cursor, cnx, url):    
    # insert into DB
    # url = "'" + url + "'"  
    # insert_db = 'INSERT INTO website(url) VALUES ({});'.format(url)
    cursor = cnx.cursor(prepared=True)
    insert_tuples = url
    print(insert_tuples)
    sql_insert_query = 'INSERT INTO website(url) VALUES (%s)'
 
    try:
        cursor.executemany(sql_insert_query, insert_tuples)
        cnx.commit()
        print(cursor.rowcount,"Insertion Successful")
    except mc.Error as err:
        cnx.rollback()
        print("Something went wrong in inserting in DB: {}".format(err))

def closeDb(cnx):
    # closes DB after operation
    try:
        cnx.close()
        print("Database Closed")
    except mc.Error as err:
        print("Something went wrong whuile closing DB: {}".format(err))
