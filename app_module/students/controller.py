from app_module import mysql

# Fetch every student data from the database
def displayAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `students` ORDER BY `last_name`, `first_name` ASC;")
        return cur.fetchall()
    except mysql.connection.Error as e:
        raise e
    
# Fetch the students according to the search parameters
def search(column, param):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `students` WHERE {column} LIKE '%{param}%';")
        return cur.fetchall()
    except mysql.connection.Error as e:
        raise e

# Fetch student based on the id parameter
def get(original_student_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `students` WHERE `student_id` = '{original_student_id}';")
        return cur.fetchone()
    except mysql.connection.Error as e:
        raise e

# Fetch the programs to be displayed in the forms
def programs():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `programs`;")
        return cur.fetchall()
    except mysql.connection.Error as e:
        raise e
    
# Add the student parameter to the database 
def add(student):
    try:
        cur = mysql.connection.cursor()
        insert_statement = ("""
                            INSERT INTO `students`(`student_id`, `first_name`, `last_name`,`program_code`, `year_level`, `gender`)
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """)
        cur.execute(insert_statement, student)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        raise e
    
# Update the record of the student parameter
def edit(student):
    try:
        cur = mysql.connection.cursor()
        edit_statement = ("""
                          UPDATE `students` 
                          SET `student_id` = %s, `first_name` = %s, `last_name` = %s, `program_code` = %s, `year_level` = %s, `gender` = %s 
                          WHERE `student_id` = %s;
                          """)
        cur.execute(edit_statement, student)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        raise e
    
# Delete the student based on the id parameter
def delete(student_id):
    try:
        cur = mysql.connection.cursor()
        delete_statement = "DELETE FROM `students` WHERE `student_id` = %s;"
        cur.execute(delete_statement, (student_id,))
        mysql.connection.commit()
        cur.close()
    except mysql.connection.Error as e:
        raise e