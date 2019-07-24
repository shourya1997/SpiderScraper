import pymysql as mc
import config

USERNAME = config.USERNAME
PASS = config.PASSWORD
DBNAME = config.DBNAME

def new_url_list(cursor, cnx, url):
    # creats a list of urls which dont exist in DB
    url_new = []
    for urls in url:
        if not urlExist(cursor, cnx, urls):
            url_new.append(urls)
        else:
            continue
    return url_new

def urlExist(cursor, cnx, url):
    # check if url exists in parsedUrl Table or not
    print("URL Passed to chech if exists or not")
    sql_find_url = "SELECT * FROM parsedUrls WHERE url in (%s)"    
    try:
        cursor.executemany(sql_find_url, (url,))
        record = cursor.fetchall()
        return record
    except mc.Error as err:
        cnx.rollback()
        print("Something went wrong in urlExist() in DB: {}".format(err))


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
    url_new = new_url_list(cursor, cnx, url)   

    insert_tuple = [(x,) for x in url_new] # converting list to tuples
    sql_insert_query = "INSERT INTO parsedUrls(url) VALUES (%s)"

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

if __name__ == "__main__":
    cursor, cnx = getDbConnection()
    # insertDb(cursor, cnx, ['qw.com','er.com','ty.com'])
    url_list = ['google.com','er.com','xyz.com']
    # for url in url_list:
    #     if urlExist(cursor, cnx, url):
    #         print(url,"Not exists")
    #     else:
    #         print("Dosent Exist")
    insertDb(cursor, cnx, url_list)
    closeDb(cursor, cnx)