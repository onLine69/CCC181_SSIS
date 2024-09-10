from flask import Blueprint

user_bp = Blueprint('programs',__name__)

from . import controller