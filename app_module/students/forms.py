from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField


class StudentForm(FlaskForm):
    id_number = StringField(label="ID Number", validators=[validators.DataRequired(message="Must have an input."), validators.length(min=9,max=9,message="Length not valid."), 
                                                           validators.Regexp(regex="\\d{4}-\\d{4}",message="Format not valid.")])
    first_name = StringField(label="First Name", validators=[validators.DataRequired(message="Must have an input."), validators.length(min=1,max=50,message="Length not valid.")])
    last_name = StringField(label="Last Name", validators=[validators.DataRequired(message="Must have an input."), validators.length(min=1,max=50,message="Length not valid.")])
    program_code = SelectField(label="Program", choices=[])
    year_level = SelectField(label="Year Level", choices=[("1st year", "1st year"), ("2nd year", "2nd year"), ("3rd year", "3rd year"), ("4th year", "4th year"), ("More...", "More...")])
    gender = StringField(label="Gender", validators=[validators.DataRequired(), validators.length(min=1,max=50,message="Length not valid.")])
    add_student = SubmitField() 