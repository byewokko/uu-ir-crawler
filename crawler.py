import re
from queue import Queue, Empty
from urllib.request import urlopen

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
        print(bool(self._urlfilter.match(url)), url)
        if url not in self._known and self._urlfilter.match(url):
            self._known.add(url)
            self._queue.put_nowait(url)
    
    def urls_from_list(self,li):
        for url in li:
            self.add_url(url.strip())
    
    def urls_from_file(self,urlfile):
        with open(urlfile,"r") as f:
            for li in f:
                self.add_url(li.strip())

    def crawl(self, maxpages, req_delay=50, max_parallel_req=5):
        # maxpages is the number of pages that will stop the crawler
        n_completed = 0
        print("Crawler started.")
        while n_completed < maxpages:
            try:
                url = self._queue.get_nowait()
            except Empty:
                break
            print(url)
            req = urlopen(url)
            yield req
        
        print("Crawler finished.")
