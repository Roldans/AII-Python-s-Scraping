#!/usr/bin/python
import sqlite3
import Tkinter
import urllib2
from Tkinter import *
from urllib2 import *
from bs4 import BeautifulSoup



##-------------------------------crawl html of a web----------------------------------------
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
    Titulo =""

    table = soup.find_all( class_=["TituloIndice", "LinkIndice"])
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

def crawl():
    url = "http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp"
    page = recuperarhtml(url)
    filtrar(page)
##------------------------------------------------------------------------------------------------------

##-------------------------------search on DB----------------------------------------
def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)


def search():

    root2 = Tkinter.Toplevel(top)
    root2.title="Categoria search"
    entry = Entry(root2)
    entry.pack()
    entry.focus_set()

    def onDBsearch():
        # Conexion con la DB
        conn = sqlite3.connect('Categorias.db')
        print "Opened database successfully";
        aux = entry.get()
        print str(aux)
        cursor = conn.execute("SELECT NAME, LINK, CATEGORIA from CATEGORIA where CATEGORIA LIKE ?", (aux,))
        imprimir_etiqueta(cursor)
        root2.destroy()
        conn.close()


    b = Button(root2, text='search', command=onDBsearch)
    b.pack(side='bottom')
    root2.mainloop()
##------------------------------------------------------------------------------------------------------

##--------------------------------------------Buscar evento-------------------------------------------------

def filtrarEvento(html, textoDeBusqueda):
    soup = BeautifulSoup(str(html), 'html.parser')
    table = soup.find_all(class_=["Sala", "Destacamos"])
    texto = textoDeBusqueda
    titulo= ""
    fecha = ""
    esTitulo = TRUE
    guardado = FALSE
    result=[["",""],]

    for a in table:
        if(a.get("class")==[u'Sala']):
            fecha = a.next
            esTiutlo= TRUE
            guardado= FALSE

        if(a.get("class")==[u'Destacamos']):
            esTitulo = TRUE
            guardado = FALSE

            for div in a.stripped_strings:

                if esTitulo:
                    titulo=div
                    esTitulo=FALSE
                if texto in div and guardado == FALSE:
                    result.append([titulo,fecha])
                    guardado = TRUE
                    break
    return result
def evento():

    #Nueva ventana y buscador
    window2 = Tkinter.Toplevel(top)
    L1 = Tkinter.Label(window2, text="key word")
    L1.pack(side=Tkinter.LEFT)
    E1 = Tkinter.Entry(window2, bd=5)
    E1.pack(side=Tkinter.RIGHT)

    def buscarC_button_action2():
        window3 = Tkinter.Toplevel(window2)
        auxtext = Tkinter.StringVar()
        aux = ""
        plainText = Tkinter.Message(window3, textvariable=auxtext)
        url = "http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp"
        page = recuperarhtml(url)

        for result in filtrarEvento(page, E1.get()):
            aux = aux + "Titulo: " + result[0] + "\nFecha: " + result[1] + "\n\n"
        auxtext.set(aux)
        plainText.pack()
        window3.minsize(width=200, height=200)
        window3.resizable(width=True, height=True)
        window3.mainloop()

    listar_button2 = Tkinter.Button(window2, text="ok", command=buscarC_button_action2, bg="blue")
    window2.minsize(width=200, height=200)
    window2.resizable(width=True, height=True)
    listar_button2.pack(side=Tkinter.BOTTOM)

    window2.mainloop()







top = Tkinter.Tk()
frame = Frame(top)
frame.pack()
AlmacenarButton = Tkinter.Button(frame, text="Almacenar Categorias", command=crawl)
ListarButton = Tkinter.Button(frame, text="Buscar Categoria", command=search)
SearchButton = Tkinter.Button(frame, text="Buscar Evento", command=evento)

AlmacenarButton.pack(side=LEFT)
ListarButton.pack(side=LEFT)
SearchButton.pack(side=LEFT)
top.mainloop()