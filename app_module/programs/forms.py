from flask_wtf import FlaskForm
from wtforms import StringField, validators, SelectField


class ProgramForm(FlaskForm):
    program_code = StringField(label="Program Code", validators=[validators.DataRequired(message="Provide a code."), validators.length(min=1,max=10,message="Length not valid, should be between 1 and 10 inclusive."), 
                                                           validators.Regexp(regex="^[A-Z]+$",message="Invalid Format: Must be all capital letters.")])
    program_name = StringField(label="Program Name", validators=[validators.DataRequired(message="Provide a name."), validators.length(min=1,max=50,message="Length not valid. should be between 1 and 50 inclusive.")])
    college_code = SelectField(label="Program", choices=[])