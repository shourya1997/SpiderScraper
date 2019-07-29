from bottle import Bottle, template, request
from crux import getDbConnection, insertDb, closeDb
import url_scraper as us
from urllib.parse import urlparse
import os


FORM_TEMPLATE = 'form.tpl'
app = Bottle()

def getDomain(url):
    '''
    Extracts Domain from the `url`
    '''
    domain = urlparse(url).hostname
    return domain

def website_list(url):
    # converting url to list
    if url.find(','):
        url_list = url.split(',')
    else:
        url_list = list(url)
    
    # stripping white spaces
    for url in url_list:
        url.strip()

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
        message = 'Website URL Submitted: ' + website_urls
        url_list = website_list(website_urls)
        domain = getDomain(website_urls)
        insertDb(cursor, cnx, url_list, domain)
        us.getLinks(website_urls, domain)
        
    return template(FORM_TEMPLATE, message=message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=port)