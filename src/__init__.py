from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import psycopg2
from flask_pymongo import PyMongo

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mongo = PyMongo()

# Import Blueprints Here
from src.user.routes import dpsm_eval_blueprint


def create_app(config_filename=None):
    
    app = Flask(__name__,template_folder='templates')
    app.config['SECRET_KEY'] = 'sample_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mjyngplqygvpak:c7867a737f6772936400cfaddfad77526d88804bd1872ec99dab1a8d338b37fc@ec2-34-200-94-86.compute-1.amazonaws.com:5432/dbrocmjjt1bb8m'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["MONGO_URI"] = "mongodb+srv://dpsmeval-admin:kfjQRPk6TjFUuS7@dpsm-eval.snak2.mongodb.net/dpsm-eval?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE"
    # Initialize app 
    db.init_app(app)

    #mongo
    mongo.init_app(app)

    login_manager.init_app(app)
    app.register_blueprint(dpsm_eval_blueprint)

    return app