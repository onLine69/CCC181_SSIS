from flask import flash, render_template, request, redirect, url_for
from app_module.colleges.controller import search as searchCollege, displayAll, add as addCollege, edit as editCollege, get, delete as deleteCollege, customErrorMessages, uploadPicture, fetchPicture, destroyPicture
from . import colleges_bp
from app_module.colleges.forms import CollegeForm
from app_module import mysql

@colleges_bp.route('/', methods=["GET"])
def index():    # The main display of the colleges
    try:
        colleges = displayAll() #fetch every college from the database

        # Fetch their profile pictures
        pics = {}   
        for college in colleges:
            pics[college[1]] = fetchPicture(college[0], college[1]) 
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")
        colleges = []   #if there is an error, display none
        pics = {}
    
    return render_template('colleges/colleges.html', pics=pics, colleges=colleges) #render the template with the data


@colleges_bp.route('/search', methods=["GET"])
def search():   # Display the searched college
    #fetch the parameters
    column_name = request.args.get('column-search', 'code')
    searched_item = request.args.get('param-search', '')
    try:
        if searched_item:
            colleges = searchCollege(column_name, searched_item)
            
            # Fetch their profile pictures
            pics = {}   
            for college in colleges:
                pics[college[1]] = fetchPicture(college[0], college[1]) 
                
            return render_template('colleges/colleges.html', pics=pics, colleges=colleges, column_name=column_name, searched_item=searched_item) 
    except mysql.connection.Error as e:
        flash(customErrorMessages(e), "danger")
    
    return redirect(url_for('colleges.index'))  #if the searched parameter is empty or an error occur, redirect to the index
    

@colleges_bp.route('/add', methods=["POST", "GET"])
def add():
    form = CollegeForm()    #initialize the form
    profile_picture_data = url_for('static', filename='images/icons/default_profile.png')

    if request.method == "POST":
        if form.validate_on_submit():
            profile_photo = request.files['profile-picture']
            alt_photo = request.form['alt-profile']
            pic_url_version = None
            
            # If the photo is not the default
            if profile_photo or not alt_photo == profile_picture_data:
                pic_url_version = uploadPicture(profile_photo, form.college_code.data)["version"]

            #create a program tuple
            college = (
                pic_url_version,
                form.college_code.data,
                form.college_name.data
            )
            
            try:
                #add the program to the database, then redirect to the index if successful
                addCollege(college)
                flash(f"College '{college[1]}' added successfully!", "success")
                return redirect(url_for('colleges.index'))
            except mysql.connection.Error as e:
                flash(customErrorMessages(e), "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")

    return render_template('colleges/collegeForms.html', form=form, profile_picture_data=profile_picture_data, page_name="Add College")


@colleges_bp.route('/edit/<original_college_code>', methods=["POST", "GET"])
def edit(original_college_code):
    original_college = get(original_college_code) #fetch the program
    original_photo_id = fetchPicture(original_college[0], original_college[1])

    if request.method == "GET":
        try:
            #if the program exist in the database, just to prevent random id numbers from the url to enter the forms
            if original_college:
                form = CollegeForm()    #initialize the form

                #set the values of the form based on the fetched program from the database
                profile_picture_data = original_photo_id
                form.college_code.data = original_college[1]
                form.college_name.data = original_college[2]
                
                return render_template('colleges/collegeForms.html', form=form, profile_picture_data=profile_picture_data, original_college_code=original_college_code, page_name="Edit College")
            else:
                #prevent the rendering of the form if the program id is invalid
                flash(f"Invalid url? Or maybe no '{original_college_code}' code available. Please don't roam around.", "danger")
        except mysql.connection.Error as e:
            flash(customErrorMessages(e), "danger")

        return redirect(url_for('colleges.index'))
    
    if request.method == "POST":
        form = CollegeForm(request.form)    #properly setup the forms incase there's an error or invalid

        if form.validate_on_submit():
            try:
                isSame = True
                pic_url_version = None
                profile_photo = request.files['profile-picture']
                alt_photo = request.form['alt-profile']

                # If the profile pic is removed
                if alt_photo == url_for('static', filename='images/icons/default_profile.png'):
                    destroyPicture(original_college_code)
                
                # If the profile pic is the same
                if not profile_photo and alt_photo == original_photo_id:
                    pic_url_version = original_college[0]

                # If the profile is changed
                if profile_photo and not profile_photo == alt_photo:
                    pic_url_version = uploadPicture(profile_photo, form.college_code.data)["version"]

                updated_college = (
                    pic_url_version,
                    form.college_code.data, 
                    form.college_name.data, 
                    original_college_code
                )

                # check if all values are the same
                for data in range(0, len(original_college)):
                    if original_college[data] != updated_college[data]:
                        isSame = False
                        break

                if not isSame:
                    editCollege(updated_college)
                    flash(f"College with now code {updated_college[1]} updated successfully!", "success")
                else:
                    flash("Nothing has been updated.", "success")

                return redirect(url_for('colleges.index'))
            except mysql.connection.Error as e:
                flash(customErrorMessages(e), "danger")
        else:
            flash("Form validation error. Please check your input.", "warning")
            
        return render_template('colleges/collegeForms.html', form=form, original_college_code=original_college_code, page_name="Edit College")
    

@colleges_bp.route('/delete/<delete_college_code>', methods=["POST", "GET"])
def delete(delete_college_code):
    if request.method == "POST":
        try:
            deleteCollege(delete_college_code)
            destroyPicture(delete_college_code)
            flash(f"College '{delete_college_code}' deleted successfully!", "success")
        except mysql.connection.Error as e:
            flash(customErrorMessages(e), "danger")
        return redirect(url_for('colleges.index'))
    else:
        #prevent direct deletion using urls
        flash(f"Delete Error: Don't just copy paste link (Not pwede), or '{delete_college_code}' code available. Please don't roam around.", "danger")
    
    return redirect(url_for('colleges.index'))