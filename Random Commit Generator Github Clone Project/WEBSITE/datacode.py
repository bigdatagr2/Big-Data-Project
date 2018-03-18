import sqlite3 as sql

con = sql.connect("database.db")


def getcur():
	global con
	cur = con.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS XDATA (data TEXT, start DATETIME, counter INTEGER, IDx integer primary key autoincrement)')

	return cur

def insertData(datax,startx,counterx):
  #  global  con = sql.connect("database.db")
    global  con
    #cur = con.cursor()
    cur = getcur()
    cur.execute("INSERT INTO XDATA (data,start,counter) VALUES (?,?,?)", (datax,startx,counterx))
    con.commit()
    con.close()
    print ("INSERTDATA : data inserted for date = ", startx)

def retrieveData():
	#con = sql.connect("database.db")
	global con
	#cur = con.cursor()
	cur = getcur()

	cur.execute("SELECT data,start,counter,idx FROM XDATA")
	users = cur.fetchall()
	con.close()
	formatted_result = [ "{idx:<5}{data:<50}{start:<10}{counter:>5}" for idx, data, start, counter in users ]
        print ("RETRIEVEDATA : nbrows = ", str(len(users)))
	idx, data, start, counter = "Id", "Post data", "Date post", "Counter"
	print('\n'.join(["{idx:<5}{data:<50}{start:<10}{counter:>5}"] + formatted_result))
	return users

def createdb():
 	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute('drop table if exists xdata;')
	cur.execute('CREATE TABLE XDATA (data TEXT, start DATETIME, counter INTEGER, IDx integer primary key autoincrement)')
	con.close()

def retrieveLast():
        #con = sql.connect("database.db")
        global con
        #cur = con.cursor()
        cur = getcur()

        cur.execute("SELECT data,start,counter,idx FROM XDATA order by idx desc limit 1;")
        users = cur.fetchall()
        con.close()
        print ("LASTDATA : Last data in database is = ", users[0],':',users[1])

        return users

