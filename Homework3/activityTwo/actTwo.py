import userAgent as ua
import re
from bs4 import BeautifulSoup
from threading import Thread
import concurrent.futures
import queue

METHOD = "GET"
VERSION = "1.1"
URL = "https://www.rit.edu/"
PORT = 443
DEPTH_LIMIT = 2
THREAD_NUM = 500
q = queue.Queue()
scannedurls = []
scannedObj = []

class URLNode:
    def __init__(self, url, depth):
        self.url = url
        self.dependencies = []
        self.depth = depth
        self.emails = []

def normalizeLinks(uri,links):
    newlinks = []
    for link in links:
        if link==None:
            pass
        elif("#" in link):
            pass
        elif("http://" in link):
            pass
        elif("https://" in link):
            if(uri.strip("https://").split("/")[0] in link):
                newlinks.append(link)
        elif bool(re.match("^/",link)):
            newurl = uri.strip("https://").split('/')[0]+link
            newurl = "https://"+newurl
            newlinks.append(newurl)
        else:
            newlinks.append(uri+"/"+link)
   
    for i in range(0,len(newlinks)):
        if "https://" not in newlinks[i]:
            newlinks[i] = "https://"+newlinks[i]
    
    newlinks = list(dict.fromkeys(newlinks))

    return newlinks

def scanURL(url):
    currURI = url.url.strip("https://").split('/',1)[0]
    currResource = url.url.strip("https://").split('/',1)
    if len(currResource)>1:
        currResource = "/"+currResource[1]
    else:
        currResource = "/"
    resp = ua.makeReq(METHOD, currResource, VERSION, currURI, PORT)
    try:
        html_doc = resp[1].decode("utf-8")
    except:
        #print("couldn't make htmldoc")
        return url
    
    #pull links
    soup = BeautifulSoup(html_doc, 'html.parser')
    aTags = soup.find_all('a')
    links = []
    for tag in aTags:
        links.append(tag.get("href"))
    links = normalizeLinks(url.url, links)
    
    #create new objects & edit curent
    newnodes = []
    for link in links:
        currentURL = URLNode(link,url.depth+1)
        newnodes.append(currentURL)
    url.dependencies = newnodes
    return url

def worker():
    while q.qsize()>0:
        item = q.get()
        print("depth: "+str(item.depth))
        print("queue size: "+str(q.qsize()))
        newobj = scanURL(item)
        newurls = newobj.dependencies
        for x in newurls:
            if x.url not in scannedurls:
                if(x.depth<=DEPTH_LIMIT):
                    q.put(x)
        scannedurls.append(newobj.url)
        scannedObj.append(newobj)
        q.task_done()

def main():
    starter = URLNode(URL,0)
    q.put(starter)

    threads = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(THREAD_NUM):
            threads.append(executor.submit(worker))
    q.join()
    print('\a')
    for x in scannedurls:
        print(x)


if __name__ == "__main__":
    main()