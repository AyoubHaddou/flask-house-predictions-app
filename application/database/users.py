from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from application import db 

class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer(), primary_key=True, unique=True, auto_increment=True)
    firstname = db.Column(db.String(length=30), nullable=False)
    lastname = db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=50),nullable=False, unique=False)
    password_hash = db.Column(db.String(length=200), nullable=False)
    
    predictions = db.relationship('Prediction', backref="User", lazy='dynamic')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print(' --------------------- saved to db')

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

def init_db():
    User( firstname= "Ayoub", 
          lastname="HADDOU", 
          email= "ayoub1@gmail.com", 
          password_hash = generate_password_hash("1234", method='sha256')
          ).save_to_db()