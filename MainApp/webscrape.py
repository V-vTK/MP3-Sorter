import requests
from bs4 import BeautifulSoup
#Code found at:
#https://stackoverflow.com/questions/61170959/python-image-scraper-not-working-properly-on-bing
#All credit to them!

def imagescrape_keyword(seartext,count):
    results=[]
    adlt = 'off' # can be set to 'moderate'
    sear=seartext.strip()
    sear=sear.replace(' ','+')
    URL='https://bing.com/images/search?q=' + sear + '&safeSearch=' + adlt + '&count=' + count
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    wow = soup.find_all('a',class_='iusc')
    for i in wow:
        try:
            results.append(eval(i['m'])['murl'])
        except:
            pass
    return results