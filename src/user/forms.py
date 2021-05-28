from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.fields.core import RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length,DataRequired, EqualTo, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .models import UserAccounts as UserAccounts
from src import login_manager
#from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields.html5 import EmailField

class PeerEvalPeer1(FlaskForm):
    item_1 = RadioField