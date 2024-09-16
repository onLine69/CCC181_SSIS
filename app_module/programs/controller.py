from app_module import mysql

# Fetch every program data from the database
def displayAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `programs` ORDER BY `name` ASC;")
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Fetch the programs according to the search parameters
def search(column, param):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `programs` WHERE {column} COLLATE utf8mb4_bin LIKE '%{param}%';")
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

# Fetch student based on the id parameter
def get(original_program_code):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `programs` WHERE `code` = '{original_program_code}';")
        return cur.fetchone()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Add the program parameter to the database 
def add(program):
    try:
        cur = mysql.connection.cursor()
        insert_statement = """
                        INSERT INTO `programs`(`code`, `name`, `college_code`)
                        VALUES (%s, %s, %s);
                        """
        cur.execute(insert_statement, program)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Update the record of the program parameter
def edit(program):
    try:
        cur = mysql.connection.cursor()
        edit_statement = """
                        UPDATE `programs` 
                        SET `code` = %s, `name` = %s, `college_code` = %s 
                        WHERE `code` = %s;
                        """
        cur.execute(edit_statement, program)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Delete the program based on the code parameter
def delete(program_code):
    try:
        cur = mysql.connection.cursor()
        delete_statement = """
                        DELETE FROM `programs` 
                        WHERE `code` = %s;
                        """
        cur.execute(delete_statement, (program_code,))
        mysql.connection.commit()
        cur.close()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed