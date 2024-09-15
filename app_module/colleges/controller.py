from app_module import mysql

# Fetch every college data from the database
def displayAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `colleges` ORDER BY `name` ASC;")
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Fetch the colleges according to the search parameters
def search(column, param):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `colleges` WHERE {column} LIKE '%{param}%';")
        return cur.fetchall()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

# Fetch college based on the id parameter
def get(original_college_code):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM `colleges` WHERE `code` = '{original_college_code}';")
        return cur.fetchone()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Add the college parameter to the database 
def add(college):
    try:
        cur = mysql.connection.cursor()
        insert_statement = """
                        INSERT INTO `colleges`(`code`, `name`)
                        VALUES (%s, %s);
                        """
        cur.execute(insert_statement, college)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Update the record of the college parameter
def edit(college):
    try:
        cur = mysql.connection.cursor()
        edit_statement = """
                    UPDATE `colleges` 
                    SET `code` = %s, `name` = %s
                    WHERE `code` = %s;
                    """
        cur.execute(edit_statement, college)
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed
    
# Delete the college based on the code parameter
def delete(college_code):
    try:
        cur = mysql.connection.cursor()
        delete_statement = """
                        DELETE FROM `colleges` 
                        WHERE `code` = %s;
                        """
        cur.execute(delete_statement, tuple(college_code))
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed