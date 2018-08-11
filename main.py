from crawler import Crawler
from parser import Parser

urlfile = "startlist.txt"
urlfilter = r"https?://cs.wikipedia.org/wiki/[\w%]*"
out = "output.txt"

def main():
    cr = Crawler(urlfile,urlfilter)
    pr = Parser(out)
    for page in cr.crawl(20):
        urls = pr.parse(page)
        cr.urls_from_list(urls)

if __name__ == "__main__":
    main()
    
