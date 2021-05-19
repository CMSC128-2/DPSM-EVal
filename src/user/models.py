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

    def __init__(self,id, first_name, middle_name, last_name, email, password, is_unit_head, is_admin, is_unit_apc, is_dept_head):
        self.id = id
        self.first_name       = first_name
        self.middle_name      = middle_name
        self.last_name        = last_name
        self.email            = email
        self.password         = password
        self.is_unit_head     = is_unit_head
        self.is_unit_apc      = is_unit_apc
        self.is_dept_head     = is_dept_head
        self.is_admin         = is_admin
