from flask import flash, render_template, request, redirect, url_for, flash
from app_module.students.controller import search as searchStudent, displayAll, add as addStudent, edit as editStudent, get, delete as deleteStudent, customErrorMessages, uploadPicture, fetchPicture, destroyPicture
from app_module.programs.controller import displayAll as programs
from . import students_bp
from app_module.students.forms import StudentForm
from app_module import mysql


@students_bp.route('/', methods=["GET"])
def index():    # The main display of the students
    try:
        students = displayAll() #fetch every student from the database

        # Fetch their profile pictures
        pics = {}   
        for student in students:
            pics[student[1]] = fetchPicture(student[0], student[1]) 
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")
        students = []   #if there is an error, display none
        pics = {}

    return render_template('students/students.html', pics=pics, students=students) #render the template with the data


@students_bp.route('/search', methods=["GET"])
def search():   # Display the searched student
    #fetch the parameters
    column_name = request.args.get('column-search', 'student_id')
    searched_item = request.args.get('param-search', '')
    try:
        if searched_item:
            # Fetch the students
            students = searchStudent(column_name, searched_item)

            # Fetch their profile pictures
            pics = {}   
            for student in students:
                pics[student[1]] = fetchPicture(student[0], student[1]) 
            
            return render_template('students/students.html', pics=pics, students=students, column_name=column_name, searched_item=searched_item) 
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")
        students = []   #if there is an error, display none
        pics = {}

    return redirect(url_for('students.index'))  #if the searched parameter is empty, redirect to the index
    

@students_bp.route('/add', methods=["POST", "GET"])
def add():
    # Initialize the form and preload the programs and the default profile picture
    form = StudentForm()
    form.program_code.choices = [(None, "Unenrolled")] + [(program[1], program[1] + '-' + program[2]) for program in programs()]
    profile_picture_data = url_for('static', filename='images/icons/default_profile.png')
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                profile_photo = request.files['profile-picture']
                alt_photo = request.form['alt-profile']
                pic_url_version = None
                
                # If the photo is not the default
                if profile_photo or not alt_photo == profile_picture_data:
                    pic_url_version = uploadPicture(profile_photo, form.id_number.data)["version"]

                student = (
                    pic_url_version,
                    form.id_number.data,
                    form.first_name.data,
                    form.last_name.data,
                    form.program_code.data if form.program_code.data != 'None' else None,
                    form.year_level.data,
                    form.gender.data
                )
                addStudent(student)
                flash(f"Student '{student[1]}' added successfully!", "success")
                return redirect(url_for('students.index'))
            except mysql.connection.Error as e:
                flash(customErrorMessages(e), "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")

    return render_template('students/studentForms.html', form=form, profile_picture_data=profile_picture_data, page_name="Add Student")



@students_bp.route('/edit/<original_student_id>', methods=["POST", "GET"])
def edit(original_student_id):
    original_student = get(original_student_id)
    original_photo_id = fetchPicture(original_student[0], original_student[1])

    if request.method == "GET":
        try:
            if original_student:
                form = StudentForm()
                form.program_code.choices = [(None, "Unenrolled")] + [(program[1], program[1] + '-' + program[2]) for program in programs()]

                profile_picture_data = original_photo_id
                form.id_number.data = original_student[1]
                form.first_name.data = original_student[2]
                form.last_name.data = original_student[3]
                form.program_code.data = original_student[4]
                form.year_level.data = original_student[5]
                form.gender.data = original_student[6]

                return render_template('students/studentForms.html', form=form, profile_picture_data=profile_picture_data, original_student_id=original_student_id, page_name="Edit Student")
            else:
                flash(f"Invalid URL or student ID '{original_student_id}' not found.", "danger")
        except mysql.connection.Error as e:
            flash(customErrorMessages(e), "danger")
        
            return redirect(url_for('students.index'))

    if request.method == "POST":
        form = StudentForm(request.form)
        form.program_code.choices = [(None, "Unenrolled")] + [(program[1], program[1] + '-' + program[2]) for program in programs()]
        
        if form.validate_on_submit():
            try:
                isSame = True
                pic_url_version = None
                profile_photo = request.files['profile-picture']
                alt_photo = request.form['alt-profile']

                # If the profile pic is removed
                if alt_photo == url_for('static', filename='images/icons/default_profile.png'):
                    destroyPicture(original_student_id)
                
                # If the profile pic is the same
                if not profile_photo and alt_photo == original_photo_id:
                    pic_url_version = original_student[0]

                # If the profile is changed
                if profile_photo and not profile_photo == alt_photo:
                    pic_url_version = uploadPicture(profile_photo, form.id_number.data)["version"]
                
                # Create the Updated Version of the student
                updated_student = (
                    pic_url_version,
                    form.id_number.data,
                    form.first_name.data,
                    form.last_name.data,
                    form.program_code.data if form.program_code.data != 'None' else None,
                    form.year_level.data,
                    form.gender.data,
                    original_student_id
                )

                # Check if there is any changes
                for info_num in range(0,len(original_student)):
                    if original_student[info_num] != updated_student[info_num]:
                        isSame = False
                        break
                
                # Only update if there is/are change/s
                if not isSame:
                    editStudent(updated_student)
                    flash(f"Student with ID '{updated_student[1]}' updated successfully!", "success")
                else:
                    flash("Nothing has been updated.", "success")
                
                return redirect(url_for('students.index'))
            except mysql.connection.Error as e:
                flash(customErrorMessages(e), "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")
            
        return render_template('students/studentForms.html', form=form, original_student_id=original_student_id, page_name="Edit Student")
    

@students_bp.route('/delete/<delete_student_id>', methods=["POST", "GET"])
def delete(delete_student_id):
    if request.method == "POST":
        try:
            deleteStudent(delete_student_id)
            destroyPicture(delete_student_id)
            flash(f"Student '{delete_student_id}' deleted successfully!", "success")
        except mysql.connection.Error as e:
            flash(customErrorMessages(e), "danger")
    else:
        #prevent direct deletion using urls
        flash(f"Delete Error: Don't just copy paste link (Not pwede), or '{delete_student_id}' ID available. Please don't roam around.", "danger")
    
    return redirect(url_for('students.index'))