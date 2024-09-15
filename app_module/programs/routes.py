from flask import flash, render_template, request, redirect, url_for
from app_module.programs.controller import search as searchProgram, displayAll, add as addProgram, edit as editProgram, get, delete as deleteProgram
from app_module.colleges.controller import displayAll as colleges
from . import programs_bp
from app_module.programs.forms import ProgramForm
from app_module import mysql


@programs_bp.route('/', methods=["GET"])
def index():    # The main display of the programs
    try:
        programs = displayAll() #fetch every program from the database
    except mysql.connection.Error as e:
        flash(f"Database error: {str(e)}", "danger")
        programs = []   #if there is an error, display none
    
    return render_template('programs/programs.html', programs=programs) #render the template with the data


@programs_bp.route('/search', methods=["GET"])
def search():   # Display the searched program
    #fetch the parameters
    column_name = request.args.get('column-search', 'code')
    searched_item = request.args.get('param-search', '')

    try:
        if searched_item:
            programs = searchProgram(column_name, searched_item)
            return render_template('programs/programs.html', programs=programs, column_name=column_name, searched_item=searched_item) 
    except mysql.connection.Error as e:
        flash(f"Database error: {str(e)}", "danger")
    
    return redirect(url_for('programs.index'))  #if the searched parameter is empty or an error occur, redirect to the index
    

@programs_bp.route('/add', methods=["POST", "GET"])
def add():
    form = ProgramForm()    #initialize the form
    form.college_code.choices = [(college[0], college[1]) for college in colleges()]    #populate the college_code dropdown based on the listed colleges

    if request.method == "POST":
        if form.validate_on_submit():
            #create a program tuple
            program = (form.program_code.data, form.program_name.data, form.college_code.data)
            
            try:
                #add the program to the database, then redirect to the index if successful
                addProgram(program)
                flash(f"Program \"{program[0]}\" added successfully!", "success")
                return redirect(url_for('programs.index'))
            except mysql.connection.Error as e:
                flash(f"Database error: {str(e)}", "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")

    return render_template('programs/programForms.html', form=form, page_name="Add Program")


@programs_bp.route('/edit/<original_program_code>', methods=["POST", "GET"])
def edit(original_program_code):
    original_program = get(original_program_code) #fetch the program
    if request.method == "GET":
        try:
            #if the program exist in the database, just to prevent random id numbers from the url to enter the forms
            if original_program:
                form = ProgramForm()    #initialize the form
                form.college_code.choices = [(college[0], college[1]) for college in colleges()]    #add the choices on the dropdown for programs dynamically
                #set the values of the form based on the fetched program from the database
                form.program_code.data = original_program[0]
                form.program_name.data = original_program[1]
                form.college_code.data = original_program[2]
                return render_template('programs/programForms.html', form=form, original_program_code=original_program_code, page_name="Edit Program")
            else:
                #prevent the rendering of the form if the program id is invalid
                flash(f"Invalid url? Or maybe no \"{original_program_code}\" code available. Please don't roam around.", "danger")
        except mysql.connection.Error as e:
            flash(f"Database error: {str(e)}", "danger")
        
        return redirect(url_for('programs.index'))
    
    if request.method == "POST":
        form = ProgramForm(request.form)    #properly setup the forms incase there's an error or invalid 
        form.college_code.choices = [(college[0], college[1]) for college in colleges()]    #add the choices on the dropdown for programs dynamically

        if form.validate_on_submit():
            try:
                isSame = True   #if nothing has changed
                updated_program = (form.program_code.data, form.program_name.data, form.college_code.data, original_program_code)
                # check if all values are the same
                for data in range(0, len(original_program)):
                    if original_program[data] != updated_program[data]:
                        isSame = False
                        break

                if (not isSame):
                    editProgram(updated_program)
                    flash(f"Program with now code {updated_program[0]} updated successfully!", "success")
                else:
                    flash("Nothing has been updated.", "success")

                return redirect(url_for('programs.index'))
            except mysql.connection.Error as e:
                flash(f"Database error: {str(e)}", "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")
            
        return render_template('programs/programForms.html', form=form, original_program_code=original_program_code, page_name="Edit Program")
    

@programs_bp.route('/delete/<delete_program_code>', methods=["POST", "GET"])
def delete(delete_program_code):
    if request.method == "POST":
        try:
            deleteProgram(delete_program_code)
            flash(f"Program \"{delete_program_code}\" deleted successfully!", "success")
        except mysql.connection.Error as e:
            flash(f"Database error: {str(e)}", "danger")
    else:
        #prevent direct deletion using urls
        flash(f"Delete Error: Don't just copy paste link (Not pwede), or \"{delete_program_code}\" code available. Please don't roam around.", "danger")
    
    return redirect(url_for('programs.index'))