from app_module import mysql

# Fetch every student data from the database
def displayAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `students` ORDER BY `last_name`, `first_name` ASC;")
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Fetch the students according to the search parameters
def search(column, param):
    try:
        cur = mysql.connection.cursor()
        if param == "Unenrolled":
            cur.execute(f"SELECT * FROM `students` WHERE {column} IS NULL;")
        else:    
            cur.execute(f"SELECT * FROM `students` WHERE {column} COLLATE utf8mb4_bin LIKE '%{param}%';")
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

# Fetch student based on the id parameter
def get(original_student_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `students` WHERE `student_id` = '{original_student_id}';")
        return cur.fetchone()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

# Add the student parameter to the database 
def add(student):
    try:
        cur = mysql.connection.cursor()
        # Prepare the insert statement
        insert_statement = """
                        INSERT INTO `students` (`student_id`, `first_name`, `last_name`, `program_code`, `year_level`, `gender`)
                        VALUES (%s, %s, %s, %s, %s, %s);
                        """
        cur.execute(insert_statement, student)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Update the record of the student parameter
def edit(student):
    try:
        cur = mysql.connection.cursor()
        edit_statement = """
                        UPDATE `students` 
                        SET `student_id` = %s, `first_name` = %s, `last_name` = %s, `program_code` = %s, `year_level` = %s, `gender` = %s 
                        WHERE `student_id` = %s;
                        """
        cur.execute(edit_statement, student)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Delete the student based on the id parameter
def delete(student_id):
    try:
        cur = mysql.connection.cursor()
        delete_statement = """
                        DELETE FROM `students` 
                        WHERE `student_id` = %s;
                        """
        cur.execute(delete_statement, (student_id,))
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def customErrorMessages(error):
    if (error.args[0] == 1062): # Check the error code first
        value = error.args[1].split("'")[1]
        if (value[4] == '-' and len(value) == 9):   # Check if the value is an id number
            return f"ID number '{value}' already exist."
        else:
            full_name = value.split("-")
            return f"Name '{full_name[0]} {full_name[1]}' already exist."
    
    return f"Something is wrong, error with code '{error.args[0]}'. \n Description: '{error.args[1]}'."