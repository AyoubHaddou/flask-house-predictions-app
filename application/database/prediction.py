from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from application import db 
import datetime

class Prediction(db.Model, UserMixin):
    __tablename__ = "Prediction"
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('User.id'))
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now())

    Neighborhood = db.Column(db.String()) 
    Overall_Cond = db.Column(db.Integer())
    Overall_Qual = db.Column(db.Integer()) 
    Kitchen_Qual = db.Column(db.String()) 
    Exter_Qual = db.Column(db.String()) 
    Garage_Cars = db.Column(db.Integer()) 
    surface_total = db.Column(db.Integer()) 
    BsmtFin_SF_first = db.Column(db.Integer()) 
    Misc_Val = db.Column(db.Integer()) 
    MS_SubClass = db.Column(db.Integer()) 
    
    price = db.Column(db.Float())
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()