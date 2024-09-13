from flask import render_template, request
from app_module.colleges.controller import search, displayAll
from . import colleges_bp


@colleges_bp.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST" and request.form["param-search"] != "":
        return render_template('colleges/colleges.html', colleges=search(request.form["column-search"], request.form["param-search"]), 
                               column_name=request.form["column-search"], searched_item=request.form["param-search"])
    else:
        return render_template('colleges/colleges.html', colleges=displayAll())