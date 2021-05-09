from app import app, db, bcrypt
from flask import Flask, render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, QuizForm, Get_Questions, Get_Results
from app.models import User, Scores
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/one")
def one():
    return render_template("topics/topic-one.html")

# TEMPORARY:

@app.route("/two")
def two():
    return render_template("topics/topic-one.html")

@app.route("/three")
def three():
    return render_template("topics/topic-one.html")

@app.route("/four")
def four():
    return render_template("topics/topic-one.html")

@app.route("/quiz", methods = ['GET','POST'])
def quiz():
    if current_user.is_authenticated:
        data = Get_Questions()

        form = QuizForm()
        if form.validate_on_submit():
            # add scores to database
            data = Get_Results()

            # remove pre-existing attempts
            Scores.query.filter(Scores.userid == current_user.id).delete()
            
            # scores are stored in the database
            scores = Scores(userid=current_user.id, questionid="q1", correct=data[0])
            db.session.add(scores)
            scores = Scores(userid=current_user.id, questionid="q2", correct=data[1])
            db.session.add(scores)
            scores = Scores(userid=current_user.id, questionid="q3", correct=data[2])
            db.session.add(scores)
            db.session.commit()
            
            return redirect(url_for('results'))
        return render_template("quiz.html", data=data, form=form)
    return redirect(url_for('login'))

@app.route("/results", methods = ['GET','POST'])
def results():
    data = Get_Results()
    score = str(sum(data)) + "/" + str(len(data))

    return render_template("results.html", data=score)

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
