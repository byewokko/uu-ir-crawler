import bs4
import lxml.etree as ET
import nltk.tokenize
#from collections import OrderedDict

class Parser():
    def __init__(self,outfile):
        self._out = open(outfile,"w")
        self._counter = 0

    def parse(self,request):
        links = []
        try:
            page = request.read().decode("utf8")
        except UnicodeDecodeError:
            print("UnicodeDecodeError")
            return []
        
        html = bs4.BeautifulSoup(page)
        content = html.find_all("div", class_= "detail__article__content")
        url = request.geturl()

        if url.startswith("https://www.lupa.cz/clanky/") and content:
            docno = str(self._counter)
            self._counter += 1

            try:
                title = html.find("h1", itemprop="headline").get_text().strip()
            except Exception as e:
                print(e)
                title = "NONE"
            
            try:
                date = html.find("span", itemprop="datePublished").get("content")[:10]
            except Exception as e:
                print(e)
                date = "NONE"
                
            try:
                author = html.find("span", itemprop="name").get_text().strip()
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
            ET.SubElement(doc, "TITLE").text = title
            ET.SubElement(doc, "DATE").text = date
            ET.SubElement(doc, "AUTHOR").text = author
            ET.SubElement(doc, "TEXT").text = text 

            tree = ET.ElementTree(doc)
            print(ET.tostring(tree, pretty_print=True, encoding = "unicode"), file=self._out)
            print("", file=self._out)
        
        for link in html.findAll("a"):
            links.append(link.get("href"))
        return links

    def clean(self, text):
        return nltk.tokenize.word_tokenize(text)
