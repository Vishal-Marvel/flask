from flask_wtf import FlaskForm
from flask_security.forms import LoginForm, RegisterForm
from wtforms import *
from wtforms.validators import *
    ## Validators
    # DataRequired
    # Email
    # EqualTo
    # InputRequired
    # IPAddress
    # Length
    # MacAddress
    # NumberRange
    # Optional
    # Regexp
    # URL
    # UUID
    # AnyOf
    # NoneOf

    ## Fields
    # BooleanField
    # DateField
    # DateTimeField
    # DecimalField
    # FileField
    # HiddenField
    # MultipleField
    # FieldList
    # FloatField
    # FormField
    # IntegerField
    # PasswordField
    # RadioField
    # SelectField
    # SelectMultipleField
    # SubmitField
    # StringField
    # TextAreaField


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()])
    email = StringField("Email Address*", validators=[DataRequired(), Email(message="Please enter a valid email address")])
    ph_no = IntegerField("Phone Number*")
    passw = PasswordField("Password*", validators=[DataRequired(), Length(min=8,message='It should have minimum of 8 characters')])
    confrm_passw = PasswordField("Conform Password*", validators=[DataRequired(), EqualTo('passw',message='Passwords must be the same'), Length(min=8,message='It should have minimum of 8 characters')])
    img = FileField("Profile Photo")
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    choices = ['User Name', 'Email Id']
    select = SelectField('Search by:', choices=choices)
    search = StringField('', validators=[DataRequired()])
    submit = SubmitField("Submit")

class ExtLoginForm(LoginForm):
	email = StringField("Email:", validators=[DataRequired(), Email(message="Please enter a valid email address")])
	password = PasswordField("Password:", validators=[DataRequired()])
	submit = SubmitField("Submit")

class Forgotform(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address")])
    submit = SubmitField("Submit")

class ForgotResetform(FlaskForm):
    code = IntegerField('Enter the code:*', validators=[DataRequired()])
    new_password = PasswordField('New Password:*', validators=[DataRequired(), Length(min=8,message='It should have minimum of 8 characters')])
    conform_password = PasswordField('New Password (again):*', validators=[DataRequired(), EqualTo('new_password',message='Passwords must be the same')])
    submit = SubmitField('Submit')
    
class Resetform(FlaskForm):
    old_password = PasswordField('Old Passsword:*', [validators.DataRequired()])
    new_password = PasswordField('New Passsword:*', [validators.DataRequired(), validators.Length(min=8,message='It should have minimum of 8 characters')])
    conform_new_password = PasswordField('Conform Passsword:*', [validators.DataRequired(), validators.EqualTo('new_password',message='Passwords must be the same')])
    submit = SubmitField("Submit")

class AuthenticateForm(FlaskForm):
    code = IntegerField('Enter the code*', validators=[DataRequired()])
    submit = SubmitField("Submit")
    