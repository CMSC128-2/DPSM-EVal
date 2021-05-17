from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import psycopg2

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Import Blueprints Here
from src.user.routes import sample_blueprint


def create_app(config_filename=None):
    
    app = Flask(__name__,template_folder='templates')
    app.config['SECRET_KEY'] = 'sample_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mjyngplqygvpak:c7867a737f6772936400cfaddfad77526d88804bd1872ec99dab1a8d338b37fc@ec2-34-200-94-86.compute-1.amazonaws.com:5432/dbrocmjjt1bb8m'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize app 
    db.init_app(app)
  
    app.register_blueprint(sample_blueprint)

    return app