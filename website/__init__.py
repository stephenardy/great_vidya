from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS","False").lower() in ['true', '1', 't']

    db.init_app(app)    
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')


    from .models import User, Subjects, UserSubjects

    Login_manager = LoginManager()
    Login_manager.login_view = 'auth.login'
    Login_manager.init_app(app)

    @Login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    return app