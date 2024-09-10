from app_module import mysql

def displayAll():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `colleges`")
    return cur.fetchall()