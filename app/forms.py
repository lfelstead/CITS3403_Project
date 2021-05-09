from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
import random

# stores questions for quiz
random.seed()
QUESTION_DATA = []

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=15)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
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

 
class QuizForm(FlaskForm):
    answer = IntegerField('answer', validators=[DataRequired()])

    submit = SubmitField('Check')
    def validate_answer(self, answer):
        if answer.data != 10:
            raise ValidationError('incorrect answer: {0} when should be 10'.format(answer.data))

def Make_Questions():
    questions = ["enter _ in the box"]
    data = []
    for question in questions:
        q = []
        for section in question.split("_"):
            q.append(section)
            q.append(random.randrange(1, 20))
        del q[-1]
        data.append(q)
    return data

def Get_Questions():
    return QUESTION_DATA

QUESTION_DATA = Make_Questions()
 
class QuizForm(FlaskForm):
    answer = IntegerField('answer', validators=[DataRequired()])

    submit = SubmitField('Check')
    def validate_answer(self, answer):
        if answer.data != QUESTION_DATA[0][1]:
            raise ValidationError('incorrect answer: {0} when should be {1}'.format(answer.data, QUESTION_DATA[0][1]))