import sys
import bs4

corpus = {}

with open("out/corpus.xml") as f:
    buffer = []
    ln = f.readline()
    while ln:
        if ln.strip() == "":
            doc = "".join(buffer)
            tree = bs4.BeautifulSoup(doc,"xml")
            corpus[int(tree.find("DOCNO").get_text())] = {
                "TITLE": tree.find("TITLE").get_text(),
                "TEXT": tree.find("TEXT").get_text()[:200]
            }
            buffer = []
        else:
            buffer.append(ln)
        
        ln = f.readline()

print(corpus[5])
