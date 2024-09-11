from app_module import mysql

def displayAll():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `students`")
    return cur.fetchall()

def search(column, param):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM `students` WHERE {column} LIKE '%{param}%'")
    
    return cur.fetchall()