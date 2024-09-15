from flask import flash, render_template, request, redirect, url_for
from app_module.colleges.controller import search as searchCollege, displayAll, add as addCollege, edit as editCollege, get, delete as deleteCollege
from . import colleges_bp
from app_module.colleges.forms import CollegeForm
from app_module import mysql

@colleges_bp.route('/', methods=["GET"])
def index():    # The main display of the colleges
    try:
        colleges = displayAll() #fetch every college from the database
    except mysql.connection.Error as e:
        flash(f"Database error: {str(e)}", "danger")
        colleges = []   #if there is an error, display none
    
    return render_template('colleges/colleges.html', colleges=colleges) #render the template with the data


@colleges_bp.route('/search', methods=["GET"])
def search():   # Display the searched college
    #fetch the parameters
    column_name = request.args.get('column-search', 'code')
    searched_item = request.args.get('param-search', '')

    try:
        if searched_item:
            colleges = searchCollege(column_name, searched_item)
            return render_template('colleges/colleges.html', colleges=colleges, column_name=column_name, searched_item=searched_item) 
    except mysql.connection.Error as e:
        flash(f"Database error: {str(e)}", "danger")
    
    return redirect(url_for('colleges.index'))  #if the searched parameter is empty or an error occur, redirect to the index
    

@colleges_bp.route('/add', methods=["POST", "GET"])
def add():
    form = CollegeForm()    #initialize the form

    if request.method == "POST":
        if form.validate_on_submit():
            #create a program tuple
            college = (form.college_code.data, form.college_name.data)
            
            try:
                #add the program to the database, then redirect to the index if successful
                addCollege(college)
                flash(f"College \"{college[0]}\" added successfully!", "success")
                return redirect(url_for('colleges.index'))
            except mysql.connection.Error as e:
                flash(f"Database error: {str(e)}", "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")

    return render_template('colleges/collegeForms.html', form=form, page_name="Add College")


@colleges_bp.route('/edit/<original_college_code>', methods=["POST", "GET"])
def edit(original_college_code):
    original_college = get(original_college_code) #fetch the program
    if request.method == "GET":
        try:
            #if the program exist in the database, just to prevent random id numbers from the url to enter the forms
            if original_college:
                form = CollegeForm()    #initialize the form
                #set the values of the form based on the fetched program from the database
                form.college_code.data = original_college[0]
                form.college_name.data = original_college[1]
                return render_template('colleges/collegeForms.html', form=form, original_college_code=original_college_code, page_name="Edit College")
            else:
                #prevent the rendering of the form if the program id is invalid
                flash(f"Invalid url? Or maybe no \"{original_college_code}\" code available. Please don't roam around.", "danger")
        except mysql.connection.Error as e:
            flash(f"Database error: {str(e)}", "danger")
        return redirect(url_for('colleges.index'))
    
    if request.method == "POST":
        form = CollegeForm(request.form)    #properly setup the forms incase there's an error or invalid

        if form.validate_on_submit():
            try:
                isSame = True   #if nothing has changed
                updated_college = (form.college_code.data, form.college_name.data, original_college_code)
                for data in range(0, len(original_college)):
                    if original_college[data] != updated_college[data]:
                        isSame = False
                        break

                if (not isSame):
                    editCollege(updated_college)
                    flash(f"College with now code {updated_college[0]} updated successfully!", "success")
                else:
                    flash("Nothing has been updated.", "success")

                return redirect(url_for('colleges.index'))
            except mysql.connection.Error as e:
                flash(f"Database error: {str(e)}", "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")
            
        return render_template('colleges/collegeForms.html', form=form, original_college_code=original_college_code, page_name="Edit College")
    

@colleges_bp.route('/delete/<delete_college_code>', methods=["POST", "GET"])
def delete(delete_college_code):
    if request.method == "POST":
        try:
            deleteCollege(delete_college_code)
            flash(f"College \"{delete_college_code}\" deleted successfully!", "success")
        except mysql.connection.Error as e:
            flash(f"Database error: {str(e)}", "danger")
        return redirect(url_for('colleges.index'))
    
    #prevent direct deletion using urls
    flash(f"Delete Error: Don't just copy paste link (Not pwede), or \"{delete_college_code}\" code available. Please don't roam around.", "danger")
    return redirect(url_for('colleges.index'))