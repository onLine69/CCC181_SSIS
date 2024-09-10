from flask import Blueprint

user_bp = Blueprint('students',__name__)

from . import controller