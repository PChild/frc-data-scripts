import requests
from bs4 import BeautifulSoup
import slff
import gen

tba = gen.setup()

def fetchDraft(post, code):
    r = requests.get(post)
    soup = BeautifulSoup(r.content,"html.parser")
    
    lines = [line.split('\t') for line in soup.pre.text.splitlines()]
    tmp = lines[:]
    
    for line in tmp:
        try:        
            assert(line[0] != "")
            assert(len(line) == 4)
            assert(not line[0].isdigit())
        except:
            lines.remove(line)
            
    tierSize = len(lines)
    return [{'Drafter': line[0].strip(), 
             'P1': (int(line[1]), idx+1), 
             'P2': (int(line[2]), 2*tierSize - idx), 
             'P3': (int(line[3]), 2*tierSize + idx + 1), 
             'Position': idx+1, 
             'Tier Size': tierSize} for idx, line in enumerate(lines)]
    
