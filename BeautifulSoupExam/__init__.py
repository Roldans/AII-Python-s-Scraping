import sqlite3
import Tkinter
import urllib2
from Tkinter import *
from urllib2 import *
from bs4 import BeautifulSoup


#Conexión y extracción de HTML
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


#Filtrado de HTML
def filtrar(html):
    soup = BeautifulSoup(str(html), 'html.parser')
    Titulo = ""

    table = soup.find_all(class_=["TituloIndice", "LinkIndice"])
    for tag in table:
        print tag.get("class")
        if tag.get("class") == [u'TituloIndice']:
            Titulo = tag.next

            if tag.get("class") == [u'LinkIndice']:
                # Conexion con la DB
                conn = sqlite3.connect('Categorias.db')
                conn.text_factory = str
                print "Opened database successfully";
                # Almacenamos los datos
                conn.execute("INSERT INTO CATEGORIA (NAME,LINK,CATEGORIA) \
                    VALUES (?,?,?);", [tag.next, tag['href'], Titulo])
                # commit y close connection
                conn.commit()
                conn.close()



#Meter en base de datos
def insertInToDB(tag):
    # Conexion con la DB
    conn = sqlite3.connect('Categorias.db')
    conn.text_factory = str
    print "Opened database successfully";
    # Almacenamos los datos
    conn.execute("INSERT INTO CATEGORIA (NAME,LINK,CATEGORIA) \
        VALUES (?,?,?);", [tag.next, tag['href'], Titulo])
    # commit y close connection
    conn.commit()
    conn.close()
