import re
import sys
import urllib
import urlparse
from bs4 import BeautifulSoup

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

def process(url,file_handler):
    print(url)
    file_handler.write(url)
    myopener = MyOpener()
    #page = urllib.urlopen(url)
    try:
        page = myopener.open(url)
    except:
        print("exception when opening url")
        return

    text = page.read()
    page.close()

    soup = BeautifulSoup(text)
    
    #f = open(name[:-4]+".links.txt",'a')
    import random
    a = soup.findAll('a', href=True)
    if len(a) > 1:
        for x in range(3):
            b = random.randint(0, len(a))
            try:
		print (urlparse.urljoin(url.strip(), a[b]['href'])+"\n")
                file_handler.write(urlparse.urljoin(url.strip(), a[b]['href'])+"\n")
            except:
                break
            
        
    #for tag in soup.findAll('a', href=True):
    #    tag['href'] = urlparse.urljoin(url, tag['href'])
        #print tag['href']
        
# process(url)

def run_extract(luxury_file):
    
    
    f1 = open(luxury_file,'r')
    f2 = open(luxury_file[:-4]+".links.txt",'w')
    
    for url in f1:
        process("http://"+url,f2)
    
    f1.close()
    f2.close()
# main()
#luxury_file = 'luxury.personas.txt'
luxury_file = 'luxury_v.txt'
#eco = 'economics.personas.txt'
eco = 'luxury_v_gdn.txt'

f1 = 'game_gdn_50.txt'
f2 = "luxury_gnd_50_ads.txt"
f3 = 'game_no_gnd_50.txt'
if __name__ == "__main__":
    #run_extract(luxury_file)
    #run_extract(eco)
    #run_extract('luxury_v_gdn59.txt')
    #run_extract(f1)
    #run_extract(f2)
    run_extract(f3)