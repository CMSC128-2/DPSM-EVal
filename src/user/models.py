from src import db,mongo
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import *
import uuid
from datetime import datetime

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

class Evaluation:
    def createRenewalEvaluation(self):
        trial_data = {
            "_id" : uuid.uuid4().hex,
            "title": "Renewal Evaluation",
            "purpose_of_evaluation": "Template shiz?",
            "start_date" : "05-24-2021",
            "end_date" : "05-26-2021",
            "release_date" : "05-27-2021",
            "participants" : [
                {
                    "user_id" : "userID1003",
                    "first_name" : "John",
                    "middle_name" : "Kevin",
                    "last_name" : "Doe",
                    "email" : "JohnDoe@gmail.com",
                    "unit" : "DPSM",
                    "status" : "Permanent",
                    "is_unit_head" : False,
                    "is_depth_head" : False,
                    "is_unit_apc" : False,
                },
                {
                    "user_id" : "userID1004",
                    "first_name" : "John",
                    "middle_name" : "Kevin",
                    "last_name" : "Doe",
                    "email" : "JohnDoe@gmail.com",
                    "unit" : "DPSM",
                    "status" : "Permanent",
                    "is_unit_head" : False,
                    "is_depth_head" : False,
                    "is_unit_apc" : False,
                },
                {
                    "user_id" : "userID1005",
                    "first_name" : "John",
                    "middle_name" : "Kevin",
                    "last_name" : "Doe",
                    "email" : "JohnDoe@gmail.com",
                    "unit" : "DPSM",
                    "status" : "Permanent",
                    "is_unit_head" : False,
                    "is_depth_head" : False,
                    "is_unit_apc" : False,
                },
            ],
            "evaluation_answers" : [
                { 
                    "user_id" : "userID1003",
                    "questions_answer" : [
                        {
                            "item_number" : 1,
                            "criteria" : "Professionalism and work ethics",
                            "answer" : 5
                        },
                                                {
                            "item_number" : 2,
                            "criteria" : "Attitude towards peers",
                            "answer" : 3
                        }
                        ,                        {
                            "item_number" : 3,
                            "criteria" : "Professionalism and work ethics",
                            "answer" : 2
                        }
                        ,                        {
                            "item_number" : 4,
                            "criteria" : "Attitude towards peers",
                            "answer" : 4
                        }
                        ,                        {
                            "item_number" : 5,
                            "criteria" : "Attitude towards the support staff",
                            "answer" : 5
                        }
                        ,                        {
                            "item_number" : 6,
                            "criteria" : "Professionalism and work ethics",
                            "answer" : 1
                        }
                    ]
                }
            ]
        }
        mongo.db.evaluation.insert_many([
            { "item": "journal", "qty": 25, "tags": ["blank", "red"], "dim_cm": [ 14, 21 ] },
            { "item": "notebook", "qty": 50, "tags": ["red", "blank"], "dim_cm": [ 14, 21 ] },
            { "item": "paper", "qty": 100, "tags": ["red", "blank", "plain"], "dim_cm": [ 14, 21 ] },
            { "item": "planner", "qty": 75, "tags": ["blank", "red"], "dim_cm": [ 22.85, 30 ] },
            { "item": "postcard", "qty": 45, "tags": ["blue"], "dim_cm": [ 10, 15.25 ] }
                ])
        #mongo.db.evaluation.insert_one(a)
