import re
from queue import Queue, Empty
from urllib.request import urlopen
import multiprocessing as mp

class Crawler():
    """
    Web crawler object.
    Maintains a list of sites, retrieves them and passes to the parser, 
    then adds newly found sites to the list.
    """
    def __init__(self, urlfile="", urlfilter=".*"):
        self._queue = Queue()
        self._known = set()
        self._urlfilter = re.compile(urlfilter)
        if urlfile:
            self.urls_from_file(urlfile)
    
    def add_url(self,url):
        if url.startswith("//"):
            url = "https:" + url
        elif url.startswith("/"):
            url = "https://www.lupa.cz" + url
        if url not in self._known and self._urlfilter.match(url):
            self._known.add(url)
            self._queue.put_nowait(url)
    
    def urls_from_list(self,li):
        for url in li:
            if url:
                self.add_url(url.strip())
    
    def urls_from_file(self,urlfile):
        with open(urlfile,"r") as f:
            for li in f:
                self.add_url(li.strip())

    def crawl(self, maxpages, workers=10):
        # maxpages is the number of pages that will stop the crawler
        n_completed = 0
        print("Crawler started.")
        while n_completed < maxpages:
            try:
                url = self._queue.get_nowait()
            except Empty:
                break
            print("CRAWLING   ", url)
            try:
                req = urlopen(url)
            except urllib.error.HTTPError as e:
                print(e)
                continue
            yield req
        
        print("Crawler finished.")
