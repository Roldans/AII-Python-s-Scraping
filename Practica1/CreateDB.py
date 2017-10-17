import sqlite3



conn = sqlite3.connect('Practica1/news.db')


conn.execute('''CREATE TABLE NEWS
         (NAME           TEXT    NOT NULL,
         LINK            TEXT    NOT NULL,
         DATE            DATE
         );''')
print "Table created successfully";

conn.close()




conn.close()
