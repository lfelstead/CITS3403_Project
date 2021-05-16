from sqlalchemy.sql.expression import desc
from app import app, db, bcrypt
from flask import Flask, render_template, flash, redirect, url_for, request
from app.forms import EditProfileForm, LoginForm, RegistrationForm, QuizForm, Make_Questions, Get_Questions, Get_Results, Get_Answers
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
    return render_template("topics/intro.html")

@app.route("/two")
def two():
    return render_template("topics/series.html")

@app.route("/three")
def three():
    return render_template("topics/parallel.html")

@app.route("/four")
def four():
    return render_template("topics/final.html")

@app.route("/quiz", methods = ['GET','POST'])
def quiz():
    if current_user.is_authenticated:
        data, images = Get_Questions()

        form = QuizForm()
        if form.validate_on_submit():
            # add scores to database
            data, _ = Get_Results()

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
        return render_template("quiz.html", data=data, images=images, form=form)
    flash('Please login to begin the quiz', 'info')
    return redirect(url_for('login'))

@app.route("/results", methods = ['GET','POST'])
def results():
    results, hints = Get_Results()
    correct = sum(results)
    if correct < 5:
        msg = "Your score is {0}/7 but that's ok. Review the different topics and reattempt the quiz.".format(correct)
    elif correct == 5:
        msg = "Your score is {0}/7. Well done! Review the different topics and reattempt the quiz.".format(correct)
    elif correct == 7:
        msg = "Your score is {0}/7. Wow a perfect score! Still, it wouldn't hurt to review the different topics and reattempt the quiz.".format(correct)
    questions, images = Get_Questions()
    answers = list(Get_Answers())
    data = list(zip(list(questions), answers, results, images, hints))
    print(answers)

    Make_Questions()
    return render_template("results.html", data=data, msg=msg, correct=correct, incorrect=len(results)-sum(results))

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        flash("Account successfully created!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Registration', form=form)

@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.is_submitted():
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user,remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Sorry, we don't have an account linked to that username and password. Please check your spelling or create an account.", "danger")
        
    return render_template('login.html', title= 'Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/references")
def references():
    return render_template('references.html')

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

@app.route("/scoreboard")
@login_required
def scoreboard():
    # get individual quiz attempts
    data = Scores.query.filter_by(userid=current_user.id).all()
    attempt_score = {}

    for quiz in data:
        if quiz.attempt not in attempt_score:
            attempt_score[quiz.attempt] = int(quiz.correct)
        else:
            attempt_score[quiz.attempt] += int(quiz.correct)

    # get every users attempts
    # sums up the total amount of correct answers for each user
    all_users = User.query.all()
    scores = []

    for userid in all_users:
        score = 0
        for item in Scores.query.filter_by(userid=userid.id).all():
            score += item.correct
        scores.append([score, userid.username])
    scores.sort(reverse=True)
    # get ranking for each user
    counter = 1
    for score in scores:
        score.append(counter)
        counter += 1

    return render_template('scoreboard.html', curr_user_scores=list(attempt_score.values()), curr_user_attempts=list(attempt_score.keys()), scores=scores)