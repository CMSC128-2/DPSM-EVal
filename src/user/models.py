from src import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import *

class to_evaluate(UserMixin, db.Model):
    to_eval_id = db.Column(db.Integer, primary_key=True)
    to_eval_first_name = db.Column(db.String(59), nullable=True)
    to_eval_middle_name = db.Column(db.String(59), nullable=True)
    to_eval_last_name = db.Column(db.String(59), nullable=True)
    to_eval_position = db.Column(db.String(59), nullable=True)
    to_eval_email = db.Column(db.String(59), nullable=True)

class evaluation_peer_eval(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evaluator = db.Column(db.Integer, nullable=False)
    evaluated = db.Column(db.Integer, nullable=False)
    evaluation_numeric = db.Column(ARRAY(Integer))
    evaluation_text = db.Column(db.String(59), nullable=True) 
    to_eval_email = db.Column(db.String(59), nullable=True) 


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
    is_evaluated_email = db.Column(ARRAY(String))


    def __init__(self, id,first_name, middle_name, last_name, work_title,unit, status, email, is_unit_head, is_unit_apc, is_dept_head):
        self.id               = id 
        self.first_name       = first_name
        self.middle_name      = middle_name
        self.last_name        = last_name
        self.work_title       = work_title
        self.status           = status
        self.email            = email
        self.unit             = unit
        self.is_unit_head     = is_unit_head
        self.is_unit_apc      = is_unit_apc
        self.is_dept_head     = is_dept_head
