from crawler import Crawler

urlfile = "startlist.txt"
urlfilter = r"https?://www.lupa.cz/(clanky|aktuality)/[^/]*/?$"
out = "out/corpus.xml"

def main():
    cr = Crawler(out, urlfile, urlfilter)
    cr.crawl(3000)

if __name__ == "__main__":
    main()
    
