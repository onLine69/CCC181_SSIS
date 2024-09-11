from app_module import app, mysql
from flask import render_template, url_for, redirect, request
from app_module.students.controller import displayAll as displayAllStudents, search as searchStudents
from app_module.programs.controller import displayAll as displayAllPrograms, search as searchPrograms
from app_module.colleges.controller import displayAll as displayAllColleges, search as searchColleges

@app.route('/')
@app.route('/students', methods=["POST", "GET"])
def studentsRoute():
    if request.method == "POST":
        search_column = request.form["column-search"]
        search_param = request.form["param-search"]
        return render_template('students.html', students=searchStudents(search_column, search_param), column_name=search_column, searched_item=search_param)
    else:
        return render_template('students.html', students=displayAllStudents())

@app.route('/programs', methods=["POST", "GET"])
def programsRoute():
    if request.method == "POST":
        search_column = request.form["column-search"]
        search_param = request.form["param-search"]
        return render_template('programs.html', programs=searchPrograms(search_column, search_param), column_name=search_column, searched_item=search_param)
    else:
        return render_template('programs.html', programs=displayAllPrograms())

@app.route('/colleges', methods=["POST", "GET"])
def collegesRoute():
    if request.method == "POST":
        search_column = request.form["column-search"]
        search_param = request.form["param-search"]
        return render_template('colleges.html', colleges=searchColleges(search_column, search_param), column_name=search_column, searched_item=search_param)
    else:
        return render_template('colleges.html', colleges=displayAllColleges())