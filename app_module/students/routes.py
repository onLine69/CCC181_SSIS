from flask import render_template, request, redirect, url_for
from app_module.students.controller import search, displayAll, programs, add as addStudent
from . import students_bp
from app_module.students.forms import StudentForm


@students_bp.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST" and request.form["param-search"] != "":
        return render_template('students/students.html', students=search(request.form["column-search"], request.form["param-search"]), 
                               column_name=request.form["column-search"], searched_item=request.form["param-search"])
    else:
        return render_template('students/students.html', students=displayAll())
    
@students_bp.route('/students/add', methods=["GET", "POST"])
def add():
    form = StudentForm()
    form.program_code.choices = [(program[0], program[1]) for program in programs()]
    if request.method == "POST" and form.is_submitted() and form.validate():
        student = (form.id_number.data, form.first_name.data, form.last_name.data, form.program_code.data, form.year_level.data, form.gender.data)
        addStudent(student)
        return redirect(url_for('students.index'))
    else:
        return render_template('students/studentForms.html', form=form)