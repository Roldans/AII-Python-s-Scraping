#!/usr/bin/python
import sqlite3
import Tkinter
import urllib2
from Tkinter import *
from urllib2 import *



URL="http://www.us.es/rss/feed/portada"


def recogerDatos():
  # Conseguimos la informacion de la pagina
    try:
        f = urllib2.urlopen(URL)
        s = f.read()
        ##Se formatea en una lista de listas [[Nombre,link,Fecha],[...,...,...]]
        l = re.findall(
            r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>',
            s)
        #cerramos conexion con la url
        return l
        f.close()
    except HTTPError, e:
        print "Ocurrio un error"
        print e.code
    except URLError, e:
        print "Ocurrio un error"
        print e.reason


def almacenar():
    l= recogerDatos()
    #Conexion con la DB
    conn = sqlite3.connect('Practica1/news.db')
    conn.text_factory = str
    print "Opened database successfully";
    #Almacenamos los datos
    for t in l:
        print t
        conn.execute("INSERT INTO NEWS (NAME,LINK,DATE) \
          VALUES (?,?,?);", [t[0],t[1],t[3]])
    #commit y close connection
    conn.commit()
    conn.close()


def listar():
    recogidos = recogerDatos()
    aux=""
    root2 = Tkinter.Toplevel(top)
    for t in recogidos:
        aux=aux+t[0]+"\n"+t[1]+"\n"+t[3]+"\n\n"

    var = StringVar(value=aux)
    aux = Message(root2, textvariable=var)
    aux.pack()
    root2.mainloop()


top = Tkinter.Tk()
frame = Frame(top)
frame.pack()
AlmacenarButton = Tkinter.Button(frame, text="Almacenar", command=almacenar)
ListarButton = Tkinter.Button(frame, text="Listar", command=listar)
SearchButton = Tkinter.Button(frame, text="Search")

AlmacenarButton.pack(side=LEFT)
ListarButton.pack(side=LEFT)
SearchButton.pack(side=LEFT)
top.mainloop()
