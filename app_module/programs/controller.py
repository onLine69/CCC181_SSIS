from cloudinary.uploader import upload, destroy
from flask import url_for
from app_module import mysql
from config import CLOUD_NAME

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
                        INSERT INTO `programs`(`profile_version`, `code`, `name`, `college_code`)
                        VALUES (%s, %s, %s, %s);
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
                        SET `profile_version` = %s, `code` = %s, `name` = %s, `college_code` = %s 
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

def customErrorMessages(error):
    if (error.args[0] == 1062): # Check the error code first
        value = error.args[1].split("'")[1]
        return f"Program Code or Name '{value}' already exist."
    
    return f"Something is wrong, error with code '{error.args[0]}'. \n Description: '{error.args[1]}'."

def uploadPicture(image_path, program_code):
    try:
        upload_result = upload(image_path, asset_folder="SSIS/Programs", public_id=program_code, invalidate=True, overwrite=True, resource_type="image", format="png")
        return upload_result
    except Exception as e:
        raise e
    
def fetchPicture(profile_version, program_code):
    return url_for('static', filename='images/icons/default_profile.png') if not profile_version else f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/v{profile_version}/{program_code}.png"

def destroyPicture(program_code):
    try:
        destroy(program_code)
    except Exception as e:
        raise e