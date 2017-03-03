import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='best930901')



cursor = conn.cursor()

cursor.execute("""create database if not exists python_db""")


cursor.close()

