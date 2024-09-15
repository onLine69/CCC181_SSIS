from flask import Blueprint

programs_bp = Blueprint('programs',__name__, template_folder='app_module/templates/programs')

from . import routes, controller, forms