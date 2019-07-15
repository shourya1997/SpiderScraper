from bottle import Bottle, template, request
from crux import getDbConnection, insertDb, closeDb
import os

FORM_TEMPLATE = 'form.tpl'
app = Bottle()

def website_list(url):
    # converting url to list
    if url.find(','):
        url_list = url.split(',')
    else:
        url_list = list(url)
    return url_list

@app.route('/')
def main():
    message = "Please enter atleast 1 website to be scraped"
    return template(FORM_TEMPLATE, message=message)

@app.route('/submit', method=['POST'])
def formhandler():
    cursor, cnx = getDbConnection()    
    """Form Page"""
    website_urls = request.forms.get('website_urls')

    if website_urls is "":
        main()
    else:
        message = 'Website URL(s) Submitted: ' + website_urls
        url_list = website_list(website_urls)
        # entering list of urls in db
        insertDb(cursor, cnx, url_list)
        
    closeDb(cnx)
    return template(FORM_TEMPLATE, message=message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=port)