import sqlite3
import Tkinter
from Tkinter import *
import tkMessageBox
from bs4 import BeautifulSoup
import urllib2
from urllib2 import *


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
def filtrar(html,url):
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
            actualResult.append(url + tag.get("href"))
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


def cargar_datos():
    conn = sqlite3.connect('foroderecho.db')
    conn.execute("DROP TABLE IF EXISTS FORO")
    conn.execute('''CREATE TABLE FORO
         (TITULO       TEXT    NOT NULL,
         LINK          TEXT    NOT NULL,
         AUTOR         TEXT    NOT NULL,
         FECHAYHORA    TEXT    NOT NULL,
         RESPUESTAS    TEXT    NOT NULL,
         VISITAS       TEXT    NOT NULL);''')
    print "Table created successfully";
    datos = FindData()
    for i in datos:
        conn.execute("""INSERT INTO FORO (TITULO, LINK, AUTOR, FECHAYHORA, RESPUESTAS, VISITAS) VALUES (?,?,?,?,?,?)""",
                     (i[0], i[1], i[2], i[3], i[4], i[5]))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM FORO")
    tkMessageBox.showinfo("Base Datos",
                          "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros.")
    conn.close()


def FindData():
    URL="https://foros.derecho.com/foro/20-Derecho-Civil-General"
    html = recuperarhtml(URL)
    urls=[URL,]

    spider=buscarPaginas(html,URL)
    contandorURLS=2
    while(contandorURLS<6):
        urls.append("https://foros.derecho.com/foro/20-Derecho-Civil-Generalforo/20-Derecho-Civil-General/page"+str(contandorURLS)+"?s=e66ad2e9bb0dd92286e8491d8edc0749")
        contandorURLS = contandorURLS +1
    datos=[]

    for a in urls:
        datosTemp =filtrar(html,a)
        print a
        for dat in datosTemp:
            datos.append(dat)
            print dat
    return datos

def buscarPaginas(html,url):
    soup = BeautifulSoup(str(html), 'html.parser')
    table = soup.findAll('a', href=re.compile('foro/20-Derecho-Civil-General/page'))
    resuls=[]
    for a in table:
        resuls.append( url+a.get('href'))
    return resuls


def showDB(window):
    # Muestra la BD
    conn = sqlite3.connect('foroderecho.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, AUTOR, FECHAYHORA FROM FORO")
    window2 = Tkinter.Toplevel(window)
    scrollbar = Tkinter.Scrollbar(window2)
    scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

    listbox = Tkinter.Listbox(window2)
    listbox.pack()

    for result in cursor:
        listbox.insert(Tkinter.END,
                       "Titulo: " + result[0] + " Autor: " + result[1] + " Fecha y Hora: " + result[2])
        listbox.insert(Tkinter.END,"")

    # attach listbox to scrollbar
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    window2.minsize(width=200, height=200)
    window2.resizable(width=True, height=True)
    window2.mainloop()
    conn.close()


def buscarTemaButtonAction(window):
    window2 = Tkinter.Toplevel(window)
    L1 = Tkinter.Label(window2, text="Tema")
    L1.pack(side=Tkinter.LEFT)
    E1 = Tkinter.Entry(window2, bd=5)
    E1.pack(side=Tkinter.RIGHT)

    def buscarC_button_action2():
        window3 = Tkinter.Toplevel(window)

        conn = sqlite3.connect('foroderecho.db')
        cursor = conn.execute("SELECT TITULO, AUTOR, FECHAYHORA from FORO where TITULO LIKE '" + E1.get() + "'")
        window2.destroy()

        scrollbar = Tkinter.Scrollbar(window3)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

        listbox = Tkinter.Listbox(window3)
        listbox.pack()

        for result in cursor:
            listbox.insert(Tkinter.END, "Titulo: " + result[0] + " Autor: " + result[1] + " Fecha y Hora: " + result[2])
            listbox.insert(Tkinter.END, "")

        conn.close()
        # attach listbox to scrollbar
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

    listar_button2 = Tkinter.Button(window2, text="ok", command=buscarC_button_action2, bg="blue")
    window2.minsize(width=200, height=200)
    window2.resizable(width=True, height=True)
    listar_button2.pack(side=Tkinter.BOTTOM)



def buscarAutorButtonAction(window):
    window2 = Tkinter.Toplevel(window)
    L1 = Tkinter.Label(window2, text="Autor")
    L1.pack(side=Tkinter.LEFT)
    E1 = Tkinter.Entry(window2, bd=5)
    E1.pack(side=Tkinter.RIGHT)

    def buscarC_button_action2():
        window3 = Tkinter.Toplevel(window)

        conn = sqlite3.connect('foroderecho.db')
        aux = E1.get()
        cursor = conn.execute("SELECT TITULO, AUTOR, FECHAYHORA from FORO where AUTOR LIKE '" + aux +"'")
        window2.destroy()

        scrollbar = Tkinter.Scrollbar(window3)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

        listbox = Tkinter.Listbox(window3)
        listbox.pack()

        for result in cursor:
            listbox.insert(Tkinter.END, "Titulo: " + result[0] + " Autor: " + result[1] + " Fecha y Hora: " + result[2])
            listbox.insert(Tkinter.END, "")

        conn.close()
        # attach listbox to scrollbar
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

    listar_button2 = Tkinter.Button(window2, text="ok", command=buscarC_button_action2, bg="blue")
    window2.minsize(width=200, height=200)
    window2.resizable(width=True, height=True)
    listar_button2.pack(side=Tkinter.BOTTOM)



def buscarFechaButtonAction(window):
    window2 = Tkinter.Toplevel(window)
    L1 = Tkinter.Label(window2, text="Fecha")
    L1.pack(side=Tkinter.LEFT)
    E1 = Tkinter.Entry(window2, bd=5)
    E1.pack(side=Tkinter.RIGHT)

    def buscarC_button_action2():
        window3 = Tkinter.Toplevel(window)

        conn = sqlite3.connect('foroderecho.db')
        aux = E1.get()
        cursor = conn.execute("SELECT TITULO, AUTOR, FECHAYHORA from FORO where FECHAYHORA LIKE '" + aux + "'")
        window2.destroy()

        scrollbar = Tkinter.Scrollbar(window3)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

        listbox = Tkinter.Listbox(window3)
        listbox.pack()

        for result in cursor:
            listbox.insert(Tkinter.END, "Titulo: " + result[0] + " Autor: " + result[1] + " Fecha y Hora: " + result[2])
            listbox.insert(Tkinter.END, "")

        conn.close()

        # attach listbox to scrollbar
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

    listar_button2 = Tkinter.Button(window2, text="ok", command=buscarC_button_action2, bg="blue")
    window2.minsize(width=200, height=200)
    window2.resizable(width=True, height=True)
    listar_button2.pack(side=Tkinter.BOTTOM)

    window2.mainloop()

def popularesButtonAction(window):
    window2 = Tkinter.Toplevel(window)
    conn = sqlite3.connect('foroderecho.db')
    cursor = conn.execute("SELECT TITULO, AUTOR, FECHAYHORA, VISITAS from FORO order by VISITAS DESC limit 5")

    listbox = Tkinter.Listbox(window2)
    listbox.pack()

    for result in cursor:
        listbox.insert(Tkinter.END, "Titulo: " + result[0] + " Autor: " + result[1] + " Fecha y Hora: " + result[2] + " Visitas: " + result[3])
        listbox.insert(Tkinter.END, "")
    conn.close()

    window2.minsize(width=200, height=200)
    window2.resizable(width=True, height=True)
    window2.mainloop()

def activosButtonAction(window):

    window2 = Tkinter.Toplevel(window)
    conn = sqlite3.connect('foroderecho.db')
    cursor = conn.execute("SELECT TITULO, AUTOR, FECHAYHORA, RESPUESTAS from FORO order by RESPUESTAS DESC limit 5")

    listbox = Tkinter.Listbox(window2)
    listbox.pack()

    for result in cursor:
        listbox.insert(Tkinter.END, "Titulo: " + result[0] + " Autor: " + result[1] + " Fecha y Hora: " + result[2] + " Respuestas: "+ result[3])
        listbox.insert(Tkinter.END, "")
    conn.close()


    window2.minsize(width=200, height=200)
    window2.resizable(width=True, height=True)
    window2.mainloop()


def main():
    window = Tkinter.Tk()
    menubar = Tkinter.Menu(window)
    datosmenu = Tkinter.Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=cargar_datos)
    datosmenu.add_command(label="Mostrar", command=lambda: showDB(window))
    datosmenu.add_separator()
    datosmenu.add_command(label="Salir", command=window.quit)
    menubar.add_cascade(label="Datos", menu=datosmenu)


    buscarmenu = Tkinter.Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Tema", command=lambda: buscarTemaButtonAction(window))
    buscarmenu.add_command(label="Autor", command=lambda: buscarAutorButtonAction(window))
    buscarmenu.add_command(label="Fecha", command=lambda: buscarFechaButtonAction(window))
    menubar.add_cascade(label="Buscar", menu=buscarmenu)


    estadisticasmenu = Tkinter.Menu(menubar, tearoff=0)
    estadisticasmenu.add_command(label="Temas mas populares", command=lambda: popularesButtonAction(window))
    estadisticasmenu.add_command(label="Temas mas activos", command=lambda: activosButtonAction(window))
    menubar.add_cascade(label="Estadisticas", menu=estadisticasmenu)

    window.config(menu=menubar)
    window.mainloop()


if __name__ == "__main__":
    main()
