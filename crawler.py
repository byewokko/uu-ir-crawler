import re
from queue import Queue, Empty
from urllib.request import urlopen
import requests
from threading import Event, Thread
import bs4
import lxml.etree as ET
import nltk.tokenize
from time import sleep

class Crawler():
    """
    Web crawler object.
    Maintains a list of sites, retrieves them and passes to the parser, 
    then adds newly found sites to the list.
    """
    def __init__(self, outfile, urlfile="", urlfilter=".*"):
        self._queue = Queue()
        self._known = set()
        self._urlfilter = re.compile(urlfilter)
        self._counter = 0
        self._target = 0
        self._out = outfile
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

    def crawl(self, maxpages, workers=12):
        # maxpages is the number of pages that will stop the crawler
        self._target = maxpages
        stopevent = Event()
        
        print("Crawler started.")
        for w in range(workers):
            worker = Thread(target=self.parse_from_queue, args=(stopevent,))
            worker.setDaemon(True)
            worker.start()
        while self._counter < self._target:
            sleep(10)
        stopevent.set()
        print("Crawler finished.")

    def parse_from_queue(self, stop):
        while not stop.is_set():
            try:
                element = self._queue.get(timeout=5)
            except Empty:
                break
            self.parse(element)
            self._queue.task_done()
        
    def parse(self, url, waittime=0.4):
        print("Processing " + url)
        try:
            req = requests.get(url, timeout=4)
        except requests.exceptions.ReadTimeout:
            return
        sleep(waittime)
        if req.status_code != 200:
            return
        links = []
        html = req.text
        
        page = bs4.BeautifulSoup(html)
        content = page.find_all("div", class_= "detail__article__content")

        if (url.startswith("https://www.lupa.cz/clanky/") or url.startswith("https://www.lupa.cz/aktuality/")) and content:
            docno = str(self._counter)
            self._counter += 1
            print(self._counter)

            try:
                title = page.find("h1", itemprop="headline").get_text().strip()
            except Exception as e:
                print(e)
                title = "NONE"
            
            try:
                date = page.find("span", itemprop="datePublished").get("content")[:10]
            except Exception as e:
                print(e)
                date = "NONE"
                
            try:
                author = page.find("span", itemprop="name").get_text().strip()
            except Exception as e:
                print(e)
                author = "NONE"

            plist = []
            for p in content[0].findAll("p"):
                text = p.get_text().strip()
                if text:
                    plist.append(" ".join(self.clean(text)))
            text = "\n".join(plist)

            doc = ET.Element("DOC")
            ET.SubElement(doc, "DOCNO").text = docno
            ET.SubElement(doc, "URL").text = url
            ET.SubElement(doc, "TITLE").text = self.clean(title)
            ET.SubElement(doc, "DATE").text = date
            ET.SubElement(doc, "AUTHOR").text = author
            ET.SubElement(doc, "TEXT").text = text 

            tree = ET.ElementTree(doc)
            #print(ET.tostring(tree, pretty_print=True, encoding = "unicode"), file=self._out)
            #self._out.write(ET.tostring(tree, pretty_print=True, encoding = "unicode"))
            with open(self._out,"a") as out:
                print(ET.tostring(tree, pretty_print=True, encoding = "unicode"), file=out)
        
        if self._counter < self._target:
            for link in page.findAll("a"):
                href = link.get("href")
                if href:
                    self.add_url(href)

    def clean(self, text):
        return nltk.tokenize.word_tokenize(text)
