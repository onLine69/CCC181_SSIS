from cloudinary.uploader import upload, destroy
from flask import url_for
from app_module import mysql
from config import CLOUD_NAME
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
        cur.execute(f"SELECT * FROM `colleges` WHERE {column} COLLATE utf8mb4_bin LIKE '%{param}%';")
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
                        INSERT INTO `colleges`(`profile_version`, `code`, `name`)
                        VALUES (%s, %s, %s);
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
                    SET `profile_version` = %s, `code` = %s, `name` = %s
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
        cur.execute(delete_statement, (college_code,))
        mysql.connection.commit()
    except mysql.connection.Error as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e
    finally:
        cur.close()  # Ensure the cursor is closed

def customErrorMessages(error):
    if (error.args[0] == 1062): # Check the error code first
        value = error.args[1].split("'")[1]
        return f"College Code or Name '{value}' already exist."
    
    return f"Something is wrong, error with code '{error.args[0]}'. \n Description: '{error.args[1]}'."

def uploadPicture(image_path, college_code):
    try:
        upload_result = upload(image_path, asset_folder="SSIS/Colleges", public_id=college_code, invalidate=True, overwrite=True, resource_type="image", format="png")
        return upload_result
    except Exception as e:
        raise e
    
def fetchPicture(profile_version, college_code):
    return url_for('static', filename='images/icons/default_profile.png') if not profile_version else f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/v{profile_version}/{college_code}.png"

def destroyPicture(college_code):
    try:
        destroy(college_code)
    except Exception as e:
        raise e
    