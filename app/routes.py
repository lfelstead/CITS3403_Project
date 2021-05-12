from sqlalchemy.sql.expression import desc
from app import app, db, bcrypt
from flask import Flask, render_template, flash, redirect, url_for, request
from app.forms import EditProfileForm, LoginForm, RegistrationForm, QuizForm, Get_Questions, Get_Results, Make_Questions, Get_Answers
from app.models import User, Scores
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

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
            # scores are stored in the database

            # Scores.query.filter(Scores.userid == current_user.id).delete()

            #Gets the last attempt by the current user, then updates it.

            try:
                attempt_count = Scores.query.filter(Scores.userid == current_user.id).order_by(desc('id')).first().attempt + 1
            except:
                attempt_count = 0

            score_list = []
            for i in range(len(data)):
                score_list.append(Scores(userid=current_user.id, questionid=f"q{i+1}", correct=data[i], attempt = attempt_count))

            db.session.add_all(score_list)
            db.session.commit()
  
            return redirect(url_for('results'))
        return render_template("quiz.html", data=data, form=form)
    return redirect(url_for('login'))

@app.route("/results", methods = ['GET','POST'])
def results():
    results = Get_Results()
    correct = sum(results)
    if correct < 2:
        msg = "Your score is {0}/3 but that ok. Review the different topics and reattempt the quiz.".format(correct)
    elif correct == 2:
        msg = "Your score is {0}/3. Well done! Review the different topics and reattempt the quiz.".format(correct)
    elif correct == 3:
        msg = "Your score is {0}/3. Wow a perfect score! Still, it wouldn't hurt to review the different topics and reattempt the quiz.".format(correct)
    questions = list(Get_Questions())
    answers = list(Get_Answers())

    Make_Questions()
    return render_template("results.html", data=zip(questions, answers), msg=msg, correct = correct, incorrect=len(results)-sum(results))

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

@app.route("/account/<username>")
@login_required
def account(username):
    user = User.query.filter(func.lower(User.username) == func.lower(username)).first_or_404()
    score = user.scores
    date = user.last_seen.strftime("%A, %B %d %Y")  
    is_current = user == current_user

    return render_template('account.html', title= 'Account', 
    user_score = score, user = user, is_current = is_current, date = date)

@app.route("/account/edit", methods = ['Get', 'POST'])
@login_required
def edit_account():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data       
        db.session.commit()
    
        flash('Your changes have been saved.')
        return redirect(url_for("account", username = current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_account.html', title= 'Edit Account', form = form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/users")
@login_required
def users():
    users_in_database = User.query.all()

    for user in users_in_database:
        print (user.username)

    return render_template('users.html', title= 'Users', all_users = users_in_database)