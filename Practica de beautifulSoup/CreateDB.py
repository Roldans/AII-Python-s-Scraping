import sqlite3



conn = sqlite3.connect('categorias.db')


conn.execute('''CREATE TABLE CATEGORIA
         (NAME           TEXT    NOT NULL,
         LINK            TEXT    NOT NULL,
         CATEGORIA       TEXT    NOT NULL);''')
print "Table created successfully";

conn.close()




conn.close()
