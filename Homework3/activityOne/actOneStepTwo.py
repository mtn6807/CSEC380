import userAgent as ua
import re
from bs4 import BeautifulSoup
import os
import threading

METHOD = "GET"
FILEPATH = "/computing/directory?term_node_tid_depth=4919"
VERSION = "1.1"
URI = "www.rit.edu"
PORT = 443

class down_img(threading.Thread):
    def __init__ (self,url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        self.__successfulDownload = downloadImg(self.url)
    def status(self):
        return self.__successfulDownload

def downloadImg(url):
    if("', '" in url):
        url = ''.join(url.split("', '"))
    url = url.strip("https://")

    uri = url.split('/')[0]
    noslash = url.split('/',1)[1]
    resources = '/'+url.split('/',1)[1]

    resp = ua.makeReq("GET", resources, VERSION, uri, PORT)
    if '302' in resp:
        return 1
    filename = noslash.split("&UN=")[1]
    filename = filename.split("&HASH")[0]
    filename +=".jpg"
    
    foldername = "./pics/"
    if not os.path.isdir(foldername):
        os.mkdir(foldername)

    filename = foldername+filename

    f = open(filename,"w+b")
    f.write(resp[1])
    f.close()
    return 0

def main():
    #make call
    resp = ua.makeReq(METHOD, FILEPATH, VERSION, URI, PORT)

    try:
        html_doc = resp[1].decode("utf-8")
    except:
        print("couldn't make htmldoc")
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    img_tags = soup.find_all('div',{"class": "views-infinite-scroll-content-wrapper clearfix"})
    img_tags = img_tags[0].find_all('img')
    urls = []
    
    threads = []
    for img in img_tags:
        urls.append(img['data-src'])
    for url in urls:
        current = down_img(url)
        threads.append(current)
        current.start()

if __name__ == "__main__":
    main()