from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from sqlalchemy import func
from app.questions import get_Questions
import re

# stores questions for quiz
QUESTION_DATA = []
ANSWERS_DATA = []
IMAGES_DATA = []
CORRECT_ANSWERS = [False, False, False, False, False, False, False]

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=15)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter(func.lower(User.username) == func.lower(username.data)).first()
        if user:
            flash('That username is taken. Please choose a different one.', 'danger')
            raise ValidationError()
        elif not bool(re.match("^[A-Za-z0-9_]*$", username.data)):
            flash('Usernames can only consist of letters, numbers and/or underscores. Please choose a different one.', 'danger')
            raise ValidationError()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('That email is taken. Please choose a different one.', 'danger')
            raise ValidationError()
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save Changes')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            #user = User.query.filter_by(username=self.username.data).first()
            user = User.query.filter(func.lower(User.username) == func.lower(self.username.data)).first()
            
            if user is not None:
                flash('That username is taken. Please choose a different one', 'danger')
                raise ValidationError()
            elif not bool(re.match("^[A-Za-z0-9_]*$", username.data)):
                flash('Usernames can only consist of letters, numbers and/or underscores. Please choose a different one', 'danger')
                raise ValidationError()


def Make_Questions():
    # reset from previous attempts
    QUESTION_DATA.clear()
    ANSWERS_DATA.clear()
    CORRECT_ANSWERS = [False, False, False]

    quest, img, ans = get_Questions()
    for index in range(len(quest)):
        QUESTION_DATA.append(quest[index])
        IMAGES_DATA.append(img[index])
        ANSWERS_DATA.append(ans[index])

# used by routes.py for quiz and results page
def Get_Questions():
    return QUESTION_DATA, IMAGES_DATA

def Get_Answers():
    return ANSWERS_DATA

def Get_Results():
    return CORRECT_ANSWERS

Make_Questions()

class QuizForm(FlaskForm):
    answer1 = RadioField('answer1', choices=[('A','A'),('B','B'), ('C','C'),('D','D')])
    answer2 = RadioField('answer2', choices=[('Yes','Yes'),('No','No')])
    answer3 = RadioField('answer3', choices=[('Yes','Yes'),('No','No')])
    answer4 = IntegerField('answer4')
    answer5 = IntegerField('answer5')
    answer6 = IntegerField('answer6')
    answer7 = IntegerField('answer7')

    submit = SubmitField('Check')

    def validate_answer1(self, answer1):
        if answer1.data == ANSWERS_DATA[0]:
            CORRECT_ANSWERS[0] = True
        else: 
            CORRECT_ANSWERS[0] = False

    def validate_answer2(self, answer2):
        if answer2.data == ANSWERS_DATA[1]:
            CORRECT_ANSWERS[1] = True
        else: 
            CORRECT_ANSWERS[1] = False
    
    def validate_answer3(self, answer3):
        if answer3.data == ANSWERS_DATA[2]:
            CORRECT_ANSWERS[2] = True
        else: 
            CORRECT_ANSWERS[2] = False
    
    def validate_answer4(self, answer4):
        print(answer4.data)