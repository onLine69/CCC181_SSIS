from flask import Blueprint, render_template, request
from app_module.students.controller import search, displayAll
from . import students_bp


@students_bp.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        search_column = request.form["column-search"]
        search_param = request.form["param-search"]
        return render_template('students/students.html', students=search(search_column, search_param), column_name=search_column, searched_item=search_param)
    else:
        return render_template('students/students.html', students=displayAll())