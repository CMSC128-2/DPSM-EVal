from src import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import *

class UserAccounts(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(59), nullable=True)
    middle_name = db.Column(db.String(59), nullable=True)
    last_name = db.Column(db.String(59), nullable=True)
    email = db.Column(db.String(59), nullable=True)
    unit = db.Column(db.String(59), nullable=True)
    status = db.Column(db.String(59), nullable=True)
    work_title = db.Column(db.String(59), nullable=True)
    is_unit_head = db.Column(db.Boolean, default=False)
    is_unit_apc = db.Column(db.Boolean, default=False)
    is_dept_head = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_evaluated_id = db.Column(ARRAY(Integer))

class to_evaluate(UserMixin, db.Model):
    to_eval_id = db.Column(db.Integer, primary_key=True)
    to_eval_first_name = db.Column(db.String(59), nullable=True)
    to_eval_middle_name = db.Column(db.String(59), nullable=True)
    to_eval_last_name = db.Column(db.String(59), nullable=True)
    to_eval_position = db.Column(db.String(59), nullable=True)
