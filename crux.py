import pymysql as mc
import config

USERNAME = config.USERNAME
PASS = config.PASSWORD
DBNAME = config.DBNAME

def checkUrlParsed(url):
    """
    Checks if given url is parsed or not
    """
    cursor, cnx = getDbConnection()
    print("URL Passed to check if parsed or not")
    sql_find_url = "SELECT * FROM parsedUrls WHERE url = %s AND parsed=False"

    try:
        cursor.execute(sql_find_url, (url,))
        record = cursor.fetchall()
        return record
    except mc.Error as err:
        cnx.rollback()
        print("Something went wrong in urlNotParsed() in DB: {}".format(err))

def urlNotParsed():
    """
    Gives list of URLs not parsed
    """
    cursor, cnx = getDbConnection()
    print("List of Not Parsed URLs")
    sql_find_url = "SELECT * FROM parsedUrls WHERE parsed=False"    
    try:
        cursor.execute(sql_find_url)
        record = cursor.fetchall()
        return record
    except mc.Error as err:
        cnx.rollback()
        print("Something went wrong in urlNotParsed() in DB: {}".format(err))

def insertScrapedUrl(url, domain, baseUrl):
    cursor, cnx = getDbConnection()
    insertDb(cursor, cnx, url, domain, baseUrl)

def new_url_list(cursor, cnx, url):
    # creats a list of urls which dont exist in DB
    url = list(url)
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
    sql_find_url = "SELECT * FROM parsedUrls WHERE url = %s"    
    try:
        cursor.execute(sql_find_url, (url,))
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

def insertDb(cursor, cnx, url, domain='DEFAULT', baseUrl='DEFAULT'):    
    # insert into DB
    url_new = new_url_list(cursor, cnx, url)   

    insert_tuple = [(x,domain,baseUrl) for x in url_new] # converting list to tuples
    sql_insert_query = "INSERT INTO parsedUrls(url, domain, parsedfrom) VALUES (%s,%s,%s)"

    try:
        cursor.executemany(sql_insert_query, insert_tuple)
        cnx.commit()
        print("Insertion Successful")
    except mc.Error as err:
        cnx.rollback()
        print("Something went wrong in inserting in DB: {}".format(err))
    finally:
        closeDb(cursor, cnx)

def updateDb(url, update):
    # Updates database
    cursor, cnx = getDbConnection()
    # if urlExist(cursor, cnx, url):
    timestamp, boolean = update[0], update[1]

    sql_update_query = 'UPDATE parsedUrls SET parsed = %s, timestamp = %s WHERE url = %s '
    update_tuple = (boolean, timestamp, url)

    try:
        cursor.execute(sql_update_query, update_tuple)
        cnx.commit()
        print("Update Successful")
    except mc.Error as err:
        cnx.rollback()
        print("Something went wrong in Updating in DB: {}".format(err))
        # finally:
        #     closeDb(cursor, cnx)
    # else:
    #     print("URL dosn't exist in DB")

def closeDb(cursor, cnx):
    # closes DB after operation
    try:
        cnx.close()
        cursor.close()
        print("Database Closed")
    except mc.Error as err:
        print("Something went wrong while closing DB: {}".format(err))

# if __name__ == "__main__":
    cursor, cnx = getDbConnection()
    # insertDb(cursor, cnx, ['qw.com','er.com','ty.com'])
    # url_list = ['google.com','er.com','xyz.com']
    # for url in url_list:
    #     if urlExist(cursor, cnx, url):
    #         print(url,"Not exists")
    #     else:
    #         print("Dosent Exist")
    # insertDb(cursor, cnx, url_list)
    # checkUrlParsed('http://app.myoperator.co')
    # closeDb(cursor, cnx)