from crawler import Crawler
from parser import Parser

urlfile = "startlist.txt"
urlfilter = r"https?://www.lupa.cz/[\w%-/]*/?"
out = "out/corpus.xml"

def main():
    cr = Crawler(urlfile,urlfilter)
    pr = Parser(out)
    for page in cr.crawl(20):
        urls = pr.parse(page)
        cr.urls_from_list(urls)

if __name__ == "__main__":
    main()
    
