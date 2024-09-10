from flask import Flask
from flask_mysqldb import MySQL
from config import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST,BOOTSTRAP_SERVE_LOCAL


mysql = MySQL()
app=Flask(__name__, instance_relative_config=True)

def start_app():    
    app.config.from_mapping(
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DB=DB_NAME,
        MYSQL_HOST=DB_HOST
    )

    mysql.init_app(app)
    
    return app


from . import routes