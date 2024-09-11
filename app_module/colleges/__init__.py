from flask import Blueprint

colleges_bp = Blueprint('colleges',__name__,  template_folder='app_module/templates/colleges')

from . import routes, controller