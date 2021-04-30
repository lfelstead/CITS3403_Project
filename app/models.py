from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    scores = db.relationship('Scores', backref='user_info', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
    
class Scores (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.Integer)
    question2 = db.Column(db.Integer)
    question3 = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Scores('{self.id}', '{self.question1}', '{self.question2}', '{self.question3}')" 
   
