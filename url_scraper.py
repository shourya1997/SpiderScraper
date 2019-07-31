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

    for link in soup.findAll('a', attrs={'href':re.compile("^https://|^http://")}):
        href = link.get('href')
        if href.find(domain) != -1:
            links.append(link.get('href'))
    print(url)
    crux.insertScrapedUrl(links,domain=domain,baseUrl=url)
    getNotParsed()

def getNotParsed():
    '''
    Gets list of URLS not scraped
    '''
    records = crux.urlNotParsed()
    print("getNotParsed Records:",records[0])
    print("getNotParsed Records:",records[1])
    urls = []
    urls.append((records[0],records[1]))
    # urls = []
    # for record in records:
    #     urls.append((record[0],record[1]))
        
    
    if len(urls) != 0:
        parseLinks(urls)
    
    else:
        print("All parsed")
        exit()

    return urls

def parseLinks(urls):
    for url, domain in urls:
        getLinks(url, domain)
        time.sleep(20)



if __name__ == "__main__":
    # url = 'https://stackoverflow.com/'
    # domain = 'stackoverflow.com'
    getNotParsed()
    


