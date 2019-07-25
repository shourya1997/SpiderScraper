from bs4 import BeautifulSoup
import requests
import re
import crux
from urllib.parse import urlparse

def getDomain(url):
    '''
    Extracts Domain from the `url`
    '''
    domain = urlparse(url).hostname
    return domain

def getLinks(url):
    ''' 
    @param: url 
    This functions extracts links from the given url
    '''
    # Update `parsed = True` for parsed url in `parsedUrls`
    # Update `domain = url.com` 
    domain = getDomain(url)
    update = [domain, True]
    crux.updateDb(url, update)

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page,'lxml')
    links = []

    for url in soup.findAll('a', attrs={'href':re.compile("^http://")}):
        links.append(url.get('href'))
    
    crux.insertScrapedUrl(links)

    getNotParsed()

def getNotParsed():
    '''
    Gets list of URLS not scraped
    '''
    records = crux.urlNotParsed()
    urls = []
    for record in records:
        urls.append(record[0])
    
    parseLinks(urls)

    return urls

def parseLinks(urls):
    for url in urls:
        getLinks(url)



# if __name__ == "__main__":
#     print(getNotParsed())
    


