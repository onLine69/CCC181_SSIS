from flask import Blueprint

user_bp = Blueprint('colleges',__name__)

from . import controller