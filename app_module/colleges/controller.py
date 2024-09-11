from app_module import mysql

def displayAll():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `colleges`")
    return cur.fetchall()

def search(column, param):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM `colleges` WHERE {column} LIKE '%{param}%'")
    
    return cur.fetchall()
