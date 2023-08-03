from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
load_dotenv()

db = SQLAlchemy()

def create_app(test=False):
    
    sqlalchemy_database_uri = os.getenv('SQLALCHEMY_DATABASE_URI_PROD')
    path_database = "application/database/database.db"
    testing = False 
    if test:
        sqlalchemy_database_uri = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')
        path_database = "application/database/test.db"
        testing = True 
        
    
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    app.config["WTF_CSRF_SECRET_KEY"] = os.getenv('WTF_CSRF_SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_database_uri
    app.config["TESTING"] = testing 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from application.database.users import User, init_db
    db.init_app(app)
    
    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from application.routes.prediction import prediction
    from application.routes.auth import auth
    app.register_blueprint(prediction)
    app.register_blueprint(auth)
    if not os.path.isfile(path_database):
        app.app_context().push()
        db.create_all()
        init_db()
        print('user added successfully')
    
    return app

app = create_app(test=True)