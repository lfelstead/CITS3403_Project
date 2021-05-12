from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from sqlalchemy import func
import random
from Equation import Expression

# stores questions for quiz
random.seed()
QUESTION_DATA = []
ANSWERS_DATA = []
CORRECT_ANSWERS = [False, False, False]

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=15)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        # user = User.query.filter_by(username=username.data).first()
        user = User.query.filter(func.lower(User.username) == func.lower(username.data)).first()


        if user:
            raise ValidationError('That username is taken. Please choose a different one')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')
    
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
                raise ValidationError('Please use a different username.')

def Make_Questions():
    # currently can make and solve equations of up to three numbers, this can be increased later if necessary
    questions = [["Q1. enter _ in the box", "x+y+z"], ["Q2. what is _ + _?", "x+y+z"], ["Q3. What is _ * _?", "x*y+z"]]
    data = []
    QUESTION_DATA.clear()
    for question, equation in questions:
        q = []
        gen_numbers = [0,0,0]
        question = question.split("_")
        for index in range(len(question)-1):
            gen_numbers[index] = random.randrange(1, 20)
            q.append(question[index])
            q.append(gen_numbers[index])
        
        q.append(question[-1])
        QUESTION_DATA.append(q)
        
        # generate equation from string and solves it with the randomly generated numbers
        eq = Expression(equation,["y","x","z"])
        ANSWERS_DATA.append(eq(gen_numbers[0], gen_numbers[1], gen_numbers[2]))

# used by routes.py for quiz and results page
def Get_Questions():
    return QUESTION_DATA

def Get_Answers():
    return ANSWERS_DATA

def Get_Results():
    return CORRECT_ANSWERS
 
class QuizForm(FlaskForm):
    answer1 = IntegerField('answer1')
    answer2 = IntegerField('answer2')
    answer3 = IntegerField('answer3')

    submit = SubmitField('Check')

    def validate_answer1(self, answer1):
        if answer1.data == ANSWERS_DATA[0]:
            CORRECT_ANSWERS[0] = True

    def validate_answer2(self, answer2):
        if answer2.data == ANSWERS_DATA[1]:
            CORRECT_ANSWERS[1] = True
    
    def validate_answer3(self, answer3):
        if answer3.data == ANSWERS_DATA[2]:
            CORRECT_ANSWERS[2] = True