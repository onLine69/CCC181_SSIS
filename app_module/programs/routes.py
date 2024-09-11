from flask import render_template, request
from app_module.programs.controller import search, displayAll
from . import programs_bp

@programs_bp.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        search_column = request.form["column-search"]
        search_param = request.form["param-search"]
        return render_template('programs/programs.html', programs=search(search_column, search_param), column_name=search_column, searched_item=search_param)
    else:
        return render_template('programs/programs.html', programs=displayAll())