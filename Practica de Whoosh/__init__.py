import Tkinter
from Tkinter import *
import tkMessageBox
from bs4 import BeautifulSoup
import urllib2
from urllib2 import *
import os

from pattern.text.en.inflect_quantify import number
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser



dirindexTemas = "IndexTemas"
dirindexRespuestas= "IndexRespuestas"


# Filtra y coge lo que queremos almacenar en la BD
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


# Filtrado de HTML
def filtrarTemas(html,url):
    url2="https://foros.derecho.com/"
    soup = BeautifulSoup(str(html), 'html.parser')
    Titulo = ""
    results=[]
    actualResult=[]
    contadorDeInfo = 0
    table = soup.find_all(class_=["title","username understate","threadstats td alt"])
    for tag in table:
        contadorDeInfo = 0
        if tag.get("class") == [u'title']:
            actualResult.append(tag.get("title"))
            actualResult.append(url2 + tag.get("href"))
        if tag.get("class") == [u'username',u'understate']:
            actualResult.append(tag.next)
            actualResult.append(tag.parent.next.next.next.next[2:])
        if tag.get("class") == [u'threadstats', u'td', u'alt']:

            for aux in tag.stripped_strings:
                if contadorDeInfo==1:
                    actualResult.append(aux)
                if contadorDeInfo==2:
                    actualResult.append(aux[9:])
                contadorDeInfo = contadorDeInfo+1
            results.append(actualResult)
            actualResult = []
    return results



def FindTemas():
    URL="https://foros.derecho.com/foro/20-Derecho-Civil-General"
    html = recuperarhtml(URL)
    urls=[URL,]
    contandorURLS=2
    while(contandorURLS<6):
        urls.append("https://foros.derecho.com/foro/20-Derecho-Civil-Generalforo/20-Derecho-Civil-General/page"+str(contandorURLS)+"?s=e66ad2e9bb0dd92286e8491d8edc0749")
        contandorURLS = contandorURLS +1
    datos=[]

    for a in urls:
        datosTemp =filtrarTemas(html,a)
        print a
        for dat in datosTemp:
            datos.append(dat)
            import unicodedata
            print (unicodedata.normalize('NFKD', dat[1]).encode('ascii','ignore'))
    return datos
def FindRespuestas(url):

    html = recuperarhtml(url)



    urls.append("https://foros.derecho.com/foro/20-Derecho-Civil-Generalforo/20-Derecho-Civil-General/page" + str(
    contandorURLS) + "?s=e66ad2e9bb0dd92286e8491d8edc0749")

    datos = []

    for a in urls:
        datosTemp = filtrarTemas(html, a)
        print a
        for dat in datosTemp:
            datos.append(dat)
            import unicodedata
            print (unicodedata.normalize('NFKD', dat[1]).encode('ascii', 'ignore'))
    return datos


def cargar_datos():

    datos = FindTemas()

        # Creamos directorio
    if not os.path.exists(dirindexTemas):
        os.mkdir(dirindexTemas)
    ix = create_in(dirindexTemas, get_schema_tema())

    #Lo abrimos
    ix = open_dir(dirindexTemas)
    #Vamos a escriir en el
    writer = ix.writer()
    i= 0
    for Tema in datos:
        writer.add_document(titulo=Tema[0],link=Tema[1],autor=Tema[2],fecha=Tema[3],respuestas=Tema[4],visitas=Tema[5])
        i+=1
        respuestas=FindRespuestas(Tema[1])
    writer.commit()
    tkMessageBox.showinfo("Fin de indexado", "Se han indexado " + str(i) + " temas")







def get_schema_tema():
    return Schema(titulo=TEXT(stored=True), link=KEYWORD(stored=True), autor=TEXT(stored=True),
                  fecha=TEXT(stored=True), respuestas=TEXT(stored=True), visitas=TEXT(stored=True))
def get_schema_respuesta():
    return Schema(titulo=TEXT(stored=True),fecha=TEXT(stored=True), autor=TEXT(stored=True)
                  , Cuerpo=TEXT(stored=True))

def main():
    window = Tkinter.Tk()
    menubar = Tkinter.Menu(window)
    datosmenu = Tkinter.Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=cargar_datos)
    window.config(menu=menubar)
    menubar.add_cascade(label="Datos", menu=datosmenu)

    window.mainloop()

main()
