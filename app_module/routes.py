from app_module import app
from flask import render_template

@app.route('/')
@app.route('/students')
def studentsRoute():
    return render_template('students.html')

@app.route('/programs')
def programsRoute():
    return render_template('programs.html')

@app.route('/colleges')
def collegesRoute():
    return render_template('colleges.html')