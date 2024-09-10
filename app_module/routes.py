from app_module import app, mysql
from flask import render_template
from app_module.students.controller import displayAll as displayAllStudents
from app_module.programs.controller import displayAll as displayAllPrograms
from app_module.colleges.controller import displayAll as displayAllColleges

@app.route('/')
@app.route('/students')
def studentsRoute():
    return render_template('students.html', students=displayAllStudents())

@app.route('/programs')
def programsRoute():
    return render_template('programs.html', programs=displayAllPrograms())

@app.route('/colleges')
def collegesRoute():
    return render_template('colleges.html', colleges=displayAllColleges())