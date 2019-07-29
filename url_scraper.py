from bs4 import BeautifulSoup
import requests
import re
import crux
import time

def getLinks(url, domain):
    ''' 
    @param: url 
    This functions extracts links from the given url
    '''
    timestamp = time.time()
    update = [timestamp, True] # Update `parsed = True` 
    crux.updateDb(url, update)

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page,'lxml')
    links = []

    for link in soup.findAll('a', attrs={'href':re.compile("^http://")}):
        href = link.get('href')
        if href.find(domain) != -1:
            links.append(link.get('href'))
    
    crux.insertScrapedUrl(links,domain=domain,baseUrl=url)
    getNotParsed()

def getNotParsed():
    '''
    Gets list of URLS not scraped
    '''
    records = crux.urlNotParsed()
    urls = []
    for record in records:
        urls.append((record[0],record[1]))
    
    parseLinks(urls)

    return urls

def parseLinks(urls):
    for url, domain in urls:
        getLinks(url, domain)



if __name__ == "__main__":
    url = 'https://myoperator.co/'
    domain = 'myoperator.co'
    getLinks(url, domain)
    


