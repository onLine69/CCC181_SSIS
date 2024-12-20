from flask import Flask
from flask_mysqldb import MySQL
from config import SECRET_KEY,DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, BOOTSTRAP_SERVE_LOCAL
from flask_wtf.csrf import CSRFProtect
import cloudinary

from dotenv import load_dotenv
load_dotenv('.env')

mysql = MySQL()
cloudnary_host = cloudinary

from app_module.students import students_bp
from app_module.programs import programs_bp
from app_module.colleges import colleges_bp

app = Flask(__name__, instance_relative_config=True)

def start_app():    
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DB=DB_NAME,
        MYSQL_HOST=DB_HOST,
        BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )

    #congfigure cloudinary
    cloudnary_host.config(secure=True)

    #register the blueprints
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(programs_bp, url_prefix="/programs")
    app.register_blueprint(colleges_bp, url_prefix="/colleges")

    mysql.init_app(app)
    CSRFProtect(app)
    return app

from . import routes