from flask import flash, render_template, request, redirect, url_for
from app_module.programs.controller import search as searchProgram, displayAll, add as addProgram, edit as editProgram, get, delete as deleteProgram, customErrorMessages, uploadPicture, fetchPicture, destroyPicture
from app_module.colleges.controller import displayAll as colleges
from . import programs_bp
from app_module.programs.forms import ProgramForm
from app_module import mysql


@programs_bp.route('/', methods=["GET"])
def index():    # The main display of the programs
    try:
        programs = displayAll() #fetch every program from the database

        # Fetch their profile pictures
        pics = {}   
        for program in programs:
            pics[program[1]] = fetchPicture(program[0], program[1]) 
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")
        programs = []   #if there is an error, display none
        pics = {}
    return render_template('programs/programs.html', pics=pics, programs=programs) #render the template with the data


@programs_bp.route('/search', methods=["GET"])
def search():   # Display the searched program
    #fetch the parameters
    column_name = request.args.get('column-search', 'code')
    searched_item = request.args.get('param-search', '')
    try:
        if searched_item:
            programs = searchProgram(column_name, searched_item)

            # Fetch their profile pictures
            pics = {}   
            for program in programs:
                pics[program[1]] = fetchPicture(program[0], program[1]) 
            return render_template('programs/programs.html', pics=pics, programs=programs, column_name=column_name, searched_item=searched_item) 
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")
        programs = []
        pics = {}
    return redirect(url_for('programs.index'))  #if the searched parameter is empty or an error occur, redirect to the index
    

@programs_bp.route('/add', methods=["POST", "GET"])
def add():
    form = ProgramForm()    #initialize the form
    form.college_code.choices = [(college[1], college[1] + '-' + college[2]) for college in colleges()]    #populate the college_code dropdown based on the listed colleges
    profile_picture_data = url_for('static', filename='images/icons/default_profile.png')

    if request.method == "POST":
        if form.validate_on_submit():
            profile_photo = request.files['profile-picture']
            alt_photo = request.form['alt-profile']
            pic_url_version = None

            # If the photo is not the default
            if profile_photo or not alt_photo == profile_picture_data:
                pic_url_version = uploadPicture(profile_photo, form.program_code.data)["version"]
            
            #create a program tuple
            program = (
                pic_url_version,
                form.program_code.data, 
                form.program_name.data, 
                form.college_code.data
            )
            
            try:
                #add the program to the database, then redirect to the index if successful
                addProgram(program)
                flash(f"Program '{program[1]}' added successfully!", "success")
                return redirect(url_for('programs.index'))
            except mysql.connection.Error as e:
                flash(customErrorMessages(e), "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")

    return render_template('programs/programForms.html', form=form, profile_picture_data=profile_picture_data, page_name="Add Program")


@programs_bp.route('/edit/<original_program_code>', methods=["POST", "GET"])
def edit(original_program_code):
    original_program = get(original_program_code) #fetch the program
    original_photo_id = fetchPicture(original_program[0], original_program[1])

    if request.method == "GET":
        try:
            #if the program exist in the database, just to prevent random id numbers from the url to enter the forms
            if original_program:
                form = ProgramForm()    #initialize the form
                form.college_code.choices = [(college[1], college[1] + '-' + college[2]) for college in colleges()]    #add the choices on the dropdown for programs dynamically
                
                #set the values of the form based on the fetched program from the database
                profile_picture_data = original_photo_id
                form.program_code.data = original_program[1]
                form.program_name.data = original_program[2]
                form.college_code.data = original_program[3]
                
                return render_template('programs/programForms.html', form=form, profile_picture_data=profile_picture_data, original_program_code=original_program_code, page_name="Edit Program")
            else:
                #prevent the rendering of the form if the program id is invalid
                flash(f"Invalid url? Or maybe no '{original_program_code}' code available. Please don't roam around.", "danger")
        except mysql.connection.Error as e:
            flash(customErrorMessages(e), "danger")
        
        return redirect(url_for('programs.index'))
    
    if request.method == "POST":
        form = ProgramForm(request.form)    #properly setup the forms incase there's an error or invalid 
        form.college_code.choices = [(college[1], college[1] + '-' + college[2]) for college in colleges()]    #add the choices on the dropdown for programs dynamically

        if form.validate_on_submit():
            try:
                isSame = True
                pic_url_version = None
                profile_photo = request.files['profile-picture']
                alt_photo = request.form['alt-profile']

                # If the profile pic is removed
                if alt_photo == url_for('static', filename='images/icons/default_profile.png'):
                    destroyPicture(original_program_code)
                
                # If the profile pic is the same
                if not profile_photo and alt_photo == original_photo_id:
                    pic_url_version = original_program[0]

                # If the profile is changed
                if profile_photo and not profile_photo == alt_photo:
                    pic_url_version = uploadPicture(profile_photo, form.program_code.data)["version"]

                updated_program = (
                    pic_url_version,
                    form.program_code.data, 
                    form.program_name.data, 
                    form.college_code.data, 
                    original_program_code
                )
                
                # check if all values are the same
                for data in range(0, len(original_program)):
                    if original_program[data] != updated_program[data]:
                        isSame = False
                        break

                if not isSame:
                    editProgram(updated_program)
                    flash(f"Program with now code {updated_program[1]} updated successfully!", "success")
                else:
                    flash("Nothing has been updated.", "success")

                return redirect(url_for('programs.index'))
            except mysql.connection.Error as e:
                flash(customErrorMessages(e), "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")

        return render_template('programs/programForms.html', form=form, original_program_code=original_program_code, page_name="Edit Program")
    

@programs_bp.route('/delete/<delete_program_code>', methods=["POST", "GET"])
def delete(delete_program_code):
    if request.method == "POST":
        try:
            deleteProgram(delete_program_code)
            destroyPicture(delete_program_code)
            flash(f"Program '{delete_program_code}' deleted successfully!", "success")
        except mysql.connection.Error as e:
            flash(customErrorMessages(e), "danger")
    else:
        #prevent direct deletion using urls
        flash(f"Delete Error: Don't just copy paste link (Not pwede), or '{delete_program_code}' code available. Please don't roam around.", "danger")
    
    return redirect(url_for('programs.index'))