from flask import Blueprint

programs_bp = Blueprint('programs',__name__)

from . import routes, controller, forms