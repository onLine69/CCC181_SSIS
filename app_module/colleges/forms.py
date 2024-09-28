from flask_wtf import FlaskForm
from wtforms import StringField, validators


class CollegeForm(FlaskForm):
    college_code = StringField(label="College Code", validators=[validators.DataRequired(message="Provide a code."), validators.length(min=1,max=5,message="Length not valid, should be between 1 and 5 inclusive."), 
                                                           validators.Regexp(regex="^[A-Z]+$",message="Invalid Format: Must be all capital letters.")])
    college_name = StringField(label="College Name", validators=[validators.DataRequired(message="Provide a name."), validators.length(min=1,max=100,message="Length not valid. should be between 1 and 100 inclusive.")])