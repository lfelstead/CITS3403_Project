from app import app, db, bcrypt
from flask import Flask, render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, QuizForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/one")
def one():
    return render_template("topic-one.html")

# TEMPORARY:

@app.route("/two")
def two():
    return render_template("topic-one.html")

@app.route("/three")
def three():
    return render_template("topic-one.html")

@app.route("/four")
def four():
    return render_template("topic-one.html")

@app.route("/quiz", methods = ['GET','POST'])
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        flash(f'correct answer.', 'success')
        return redirect(url_for('home'))
    return render_template("quiz.html", form=form)

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data}.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Registration', form=form)

@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        
    return render_template('login.html', title= 'Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
