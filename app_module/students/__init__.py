from flask import Blueprint

students_bp = Blueprint("students",__name__, template_folder="app_module/templates/students")

from . import routes, controller
