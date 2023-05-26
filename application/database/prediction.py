from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from application import db 
import datetime

to_keep = ['overall_qual', 'neighborhood_int', 'ms_subclass', 'gr_liv_area',
    'misc_val', 'kitchen_qual_int', 'bsmtfin_sf_1', 'garage_cars',
    'overall_cond', 'exter_qual_int']

class Prediction(db.Model, UserMixin):
    __tablename__ = "Prediction"
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('User.id'))
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now())
    overall_qual = db.Column(db.Integer())
    neighborhood = db.Column(db.String()) 
    ms_subclass = db.Column(db.String())
    gr_liv_area = db.Column(db.Integer())
    misc_val = db.Column(db.Integer())
    kitchen_qual = db.Column(db.String()) 
    bsmtfin_sf_1 = db.Column(db.Integer())
    garage_cars = db.Column(db.Integer())
    overall_cond = db.Column(db.Integer())
    exter_qual = db.Column(db.String())

    price = db.Column(db.Integer()) 
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()