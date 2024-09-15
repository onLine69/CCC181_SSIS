from flask import flash, render_template, request, redirect, url_for, flash
from app_module.students.controller import search as searchStudent, displayAll, add as addStudent, edit as editStudent, get, delete as deleteStudent
from app_module.programs.controller import displayAll as programs
from . import students_bp
from app_module.students.forms import StudentForm
from app_module import mysql


@students_bp.route('/', methods=["GET"])
def index():    # The main display of the students
    try:
        students = displayAll() #fetch every student from the database
    except mysql.connection.Error as e:
        flash(f"Database error: {str(e)}", "danger")
        students = []   #if there is an error, display none
    
    return render_template('students/students.html', students=students) #render the template with the data


@students_bp.route('/search', methods=["GET"])
def search():   # Display the searched student
    #fetch the parameters
    column_name = request.args.get('column-search', 'student_id')
    searched_item = request.args.get('param-search', '')

    try:
        if searched_item:
            students = searchStudent(column_name, searched_item)
            return render_template('students/students.html', students=students, column_name=column_name, searched_item=searched_item) 
    except mysql.connection.Error as e:
        flash(f"Database error: {str(e)}", "danger")
    
    return redirect(url_for('students.index'))  #if the searched parameter is empty, redirect to the index
    

@students_bp.route('/add', methods=["POST", "GET"])
def add():
    form = StudentForm()  # Initialize the form
    form.program_code.choices = [(None, "Unenrolled")] + [(program[0], program[1]) for program in programs()]  # Populate dropdown with the null value

    if request.method == "POST":
        if form.validate_on_submit():
            # Convert form data to tuple and handle NULL values
            student = (
                form.id_number.data,
                form.first_name.data,
                form.last_name.data,
                form.program_code.data if form.program_code.data != 'None' else None,   #yawa string ang pagbasa sa None gikan sa forms
                form.year_level.data,
                form.gender.data
            )

            try:
                # Add the student to the database
                addStudent(student)
                flash(f"Student \"{student[0]}\" added successfully!", "success")
                return redirect(url_for('students.index'))
            except mysql.connection.Error as e:
                flash(f"Database error: {str(e)}", "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")

    return render_template('students/studentForms.html', form=form, page_name="Add Student")


@students_bp.route('/edit/<original_student_id>', methods=["POST", "GET"])
def edit(original_student_id):
    original_student = get(original_student_id) #fetch the student

    if request.method == "GET":
        try:
            #if the student exist in the database, just to prevent random id numbers from the url to enter the forms
            if original_student:
                form = StudentForm()    #initialize the form
                form.program_code.choices = [(None, "Unenrolled")] + [(program[0], program[1]) for program in programs()]    #add the choices on the dropdown for programs dynamically
                #set the values of the form based on the fetched student from the database
                form.id_number.data = original_student[0]
                form.first_name.data = original_student[1]
                form.last_name.data = original_student[2]
                form.program_code.data = original_student[3] if original_student[3] else None
                form.year_level.data = original_student[4]
                form.gender.data = original_student[5]
                return render_template('students/studentForms.html', form=form, original_student_id=original_student_id, page_name="Edit Student")
            else:
                #prevent the rendering of the form if the student id is invalid
                flash(f"Invalid url? Or maybe no \"{original_student_id}\" ID available. Please don't roam around.", "danger")
        except mysql.connection.Error as e:
            flash(f"Database error: {str(e)}", "danger")
        
        return redirect(url_for('students.index'))
    
    if request.method == "POST":
        form = StudentForm(request.form)    #properly setup the forms incase there's an error or invalid 
        form.program_code.choices = [(None, "Unenrolled")] + [(program[0], program[1]) for program in programs()]   #add the choices on the dropdown for programs dynamically

        if form.validate_on_submit():
            try:
                isSame = True   #if nothing has changed
                updated_student = (
                    form.id_number.data,
                    form.first_name.data,
                    form.last_name.data,
                    form.program_code.data if form.program_code.data != 'None' else None,   #yawa string ang pagbasa sa None gikan sa forms
                    form.year_level.data,
                    form.gender.data, 
                    original_student_id
                )
                # check if all values are the same
                for data in range(0, len(original_student)):
                    if original_student[data] != updated_student[data]:
                        isSame = False
                        break

                if (not isSame):    #only update when something changed
                    editStudent(updated_student)
                    flash(f"Student with now ID {updated_student[0]} updated successfully!", "success")
                else:
                    flash("Nothing has been updated.", "success")

                return redirect(url_for('students.index'))
            except mysql.connection.Error as e:
                flash(f"Database error: {str(e)}", "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")
            
        return render_template('students/studentForms.html', form=form, original_student_id=original_student_id, page_name="Edit Student")
    

@students_bp.route('/delete/<delete_student_id>', methods=["POST", "GET"])
def delete(delete_student_id):
    if request.method == "POST":
        try:
            deleteStudent(delete_student_id)
            flash(f"Student \"{delete_student_id}\" deleted successfully!", "success")
        except mysql.connection.Error as e:
            flash(f"Database error: {str(e)}", "danger")
    else:
        #prevent direct deletion using urls
        flash(f"Delete Error: Don't just copy paste link (Not pwede), or \"{delete_student_id}\" ID available. Please don't roam around.", "danger")
    
    return redirect(url_for('students.index'))