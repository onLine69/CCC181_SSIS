from app_module import mysql

def displayAll():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `students`")
    return cur.fetchall()

def search(column, param):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM `students` WHERE {column} LIKE '%{param}%'")
    return cur.fetchall()

def programs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `programs`")
    return cur.fetchall()

def add(student):
    cur = mysql.connection.cursor()
    insert_statement = ("INSERT INTO `students`(`student_id`, `first_name`, `last_name`,`program_code`, `year_level`, `gender`) \
                        VALUES (%s, %s, %s, %s, %s, %s)")
    cur.execute(insert_statement, student)
    mysql.connection.commit()