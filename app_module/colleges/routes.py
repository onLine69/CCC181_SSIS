from flask import render_template, request
from app_module.colleges.controller import search, displayAll
from . import colleges_bp

@colleges_bp.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        search_column = request.form["column-search"]
        search_param = request.form["param-search"]
        return render_template('colleges/colleges.html', colleges=search(search_column, search_param), column_name=search_column, searched_item=search_param)
    else:
        return render_template('colleges/colleges.html', colleges=displayAll())