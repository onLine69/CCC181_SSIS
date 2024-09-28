from flask import Blueprint

colleges_bp = Blueprint('colleges',__name__)

from . import routes, controller, forms