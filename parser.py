import bs4

class Parser():
    def __init__(self,outfile):
        self._out = open(outfile,"w")

    def parse(self,request):
        links = []
        try:
            page = request.read().decode("utf8")
        except UnicodeDecodeError:
            return []
        
        html = bs4.BeautifulSoup(page)
        content = html.select('div[id="content"]')
        if not content:
            return []
        for p in content[0].findAll("p"):
            print(self.clean(p), file=self._out)
        
        for link in content[0].findAll("a"):
            if "href" in link:
                links.append(link["href"])
        return links

    def clean(self, text):
        return text
