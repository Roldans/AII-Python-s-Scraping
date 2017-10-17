import urllib2
import bs4
from bs4 import BeautifulSoup
from urllib2 import *


# Take the html form de page
def recuperarhtml(url):
    try:
        f = urllib2.urlopen(url)
        page = f.read()
        f.close()
        return page

    except HTTPError, e:
        print "Ocurrio un error"
        print e.code
    except URLError, e:
        print "Ocurrio un error"
        print e.reason
    except ValueError, e:

        print e.message


# take the urls from the html
def filtrar(html):
    soup = BeautifulSoup(str(html), 'html.parser')

    anchors = soup.findAll('a', href=re.compile('http'))
    links = set()

    for anchor in anchors:
        links.add(anchor['href'])


    return links


def crawl(url,cont):
    page = recuperarhtml(url)
    results = filtrar(page)

    resultfinal = set(results)

    if(cont>0):
        for result in results:
            aux = set(crawl(result, cont-1))

            resultfinal.union(aux)
    return resultfinal







# INICIO DEL PROGRAMA
URL = "http://www.finofilipino.org"

result = crawl(URL,1)
file_object = open("urls.txt", "w")
for a in result:
    print a
    # encodea!!!! el texto
    file_object.write(a + "\n")