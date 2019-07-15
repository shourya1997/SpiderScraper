import pymysql as mc
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
    insert_tuple = [(x,) for x in url] # converting list to tuples
    sql_insert_query = "INSERT INTO website(url) VALUES (%s)"
 
    try:
        cursor.executemany(sql_insert_query, insert_tuple)
        cnx.commit()
        print("Insertion Successful")
    except mc.Error as err:
        cnx.rollback()
        print("Something went wrong in inserting in DB: {}".format(err))

def closeDb(cursor, cnx):
    # closes DB after operation
    try:
        cnx.close()
        cursor.close()
        print("Database Closed")
    except mc.Error as err:
        print("Something went wrong while closing DB: {}".format(err))

# if __name__ == "__main__":
#     cursor, cnx = getDbConnection()
#     insertDb(cursor, cnx, ['qw.com','er.com','ty.com'])
#     closeDb(cursor, cnx)