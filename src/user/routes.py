from flask import Blueprint, render_template, session, redirect, abort, request, url_for, flash,jsonify
from sqlalchemy.sql.expression import true,func
from pyasn1.type.univ import Null
import requests
import flask
from flask.globals import request
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from google import auth
import google
from google.auth import credentials
from werkzeug.utils import cached_property
from .models import Evaluation, UserAccounts, to_evaluate, questions_peer_eval, questions_self_eval
from src import login_manager,db, mongo
from google_auth_oauthlib.flow import Flow
import google.oauth2.id_token as id_token
import os
import pip._vendor.cachecontrol as cacheControl
import uuid
GOOGLE_CLIENT_ID = "509870006288-jrkbji4gr3bsu9qmk9990f39uop3545c.apps.googleusercontent.com"
client_secrets_file = "src/user/google-oauth-creds.json"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
	client_secrets_file = client_secrets_file,
	scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
	redirect_uri = "http://127.0.0.1:5000/callback")


# Set up a Blueprint
dpsm_eval_blueprint = Blueprint('dpsm_eval_blueprint', __name__)

login_manager.login_view = 'dpsm_eval_blueprint.index'
@login_manager.user_loader
def load_user(user_id):
	return UserAccounts.query.get(int(user_id))

@dpsm_eval_blueprint.route('/')
def index():
	return render_template('login-page.html')

@dpsm_eval_blueprint.route('/login')
def login():
	authorization_url, state = flow.authorization_url()
	
	session["state"] = state
	return redirect(authorization_url)

@dpsm_eval_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dpsm_eval_blueprint.index'))

@dpsm_eval_blueprint.route('/callback')
def callback():
	flow.fetch_token(authorization_response=request.url)

	#if not session["state"] == request.args["state"]:
		#abort(500)
		
	credentials = flow.credentials
	request_session = requests.Session()
	cached_session = cacheControl.CacheControl(request_session)
	token_request = google.auth.transport.requests.Request(session = cached_session)

	id_info = id_token.verify_oauth2_token(
		id_token = credentials._id_token,
		request = token_request,
		audience = GOOGLE_CLIENT_ID
	)
	#return id_info
	
	session["google_id"] = id_info.get("sub")
	session["name"] = id_info.get("name")
	session["email"] = id_info.get("email")
	session["picture"] = id_info.get("picture")
	#email = id_info.get("email")
	

	#print(session["picture"])
	user = UserAccounts.query.filter_by(email=id_info.get("email")).first()
	login_user(user)
	if user is not None:
		if user.is_admin == False:
			return redirect('/user-dashboard')
		else:
			return redirect('/admin-dashboard')
	else:
		return "Faculty Account Does not Exist in Database"

@dpsm_eval_blueprint.route('/user-dashboard')
#@login_required
def dashboard():
	active_forms = []

	active_data = mongo.db.evaluation.find({"is_active" : True})

	for document in active_data:	
		active_forms.append(document)
		print(document)
	return render_template('user-faculty/dashboard.html', active_forms = active_forms)

@dpsm_eval_blueprint.route('/faculty_list/<string:form_id>/home', methods=['GET', 'POST'])
#@login_required
def faculty_list(form_id):
	this_form = mongo.db.evaluation.find({"_id" : form_id})
	evaluatees = {}
	evaluated = []
	need_to_be_evaluated = []
	need_to_be_evaluated_email = []
	current = mongo.db.evaluation.distinct('evaluatees')
	for i in this_form:
		evaluatees = i['evaluatees']
	
	for i in evaluatees:
		need_to_be_evaluated.append(i['first_name']+ ' ' + i['middle_name']+ ' ' + i['last_name'])
		need_to_be_evaluated_email.append(i['email'])

	# for i in current:
		# need_to_be_evaluated.append(i['first_name']+ ' ' + i['middle_name']+ ' ' + i['last_name'])
	
	return render_template('user-faculty/user-faculty-list.html', evaluated=evaluated, not_evaluated=zip(need_to_be_evaluated,need_to_be_evaluated_email), form_id=form_id)

###############################################################################################
#USER TEMPLATES

#PEER EVAL PAGES
@dpsm_eval_blueprint.route('/faculty/peer-eval-page-1<string:evaluated_email><string:form_id>/evaluate/', methods=['GET', 'POST'])
def peer_eval_page_1(evaluated_email, form_id):
	evaluated = user = UserAccounts.query.filter_by(email=evaluated_email).first()
	rubric = questions_peer_eval.query.filter_by(criteria='Professionalism and work ethics')

	if request.method == "POST":
		session['peer_eval_1'] = request.form.get('peer_eval_1')
		session['peer_eval_2'] = request.form.get('peer_eval_2')
		session['peer_eval_3'] = request.form.get('peer_eval_3')
		session['peer_eval_4'] = request.form.get('peer_eval_4')
		session['peer_eval_5'] = request.form.get('peer_eval_5')
		session['peer_eval_6'] = request.form.get('peer_eval_6')
		print(session['peer_eval_1'])
		return redirect(url_for('dpsm_eval_blueprint.peer_eval_page_2', evaluated_email = evaluated_email, form_id=form_id)) 

	return render_template('user-faculty/peer-eval-pages/user-peer-eval-1.html', evaluated=evaluated, rubric=rubric, form_id=form_id)

@dpsm_eval_blueprint.route('/faculty/peer-eval-page-2<string:evaluated_email><string:form_id>/evaluate/', methods=['GET', 'POST'])
def peer_eval_page_2(evaluated_email, form_id):
	evaluated = user = UserAccounts.query.filter_by(email=evaluated_email).first()
	rubric = questions_peer_eval.query.filter_by(criteria='Attitude towards students')

	if request.method == "POST":
		session['peer_eval_7'] = request.form.get('peer_eval_7')
		print(session['peer_eval_7'])
		return redirect(url_for('dpsm_eval_blueprint.peer_eval_page_3', evaluated_email = evaluated_email, form_id = form_id)) 

	return render_template('user-faculty/peer-eval-pages/user-peer-eval-2.html', evaluated=evaluated, rubric=rubric, form_id=form_id)

@dpsm_eval_blueprint.route('/faculty/peer-eval-page-3<string:evaluated_email><string:form_id>/evaluate/', methods=['GET', 'POST'])
def peer_eval_page_3(evaluated_email, form_id):
	evaluated = user = UserAccounts.query.filter_by(email=evaluated_email).first()
	rubric = questions_peer_eval.query.filter_by(criteria='Attitude towards peers')

	if request.method == "POST":
		session['peer_eval_8'] = request.form.get('peer_eval_8')
		session['peer_eval_9'] = request.form.get('peer_eval_9')
		print("fdfgdf")
		return redirect(url_for('dpsm_eval_blueprint.peer_eval_page_4', evaluated_email = evaluated_email, rubric=rubric, form_id=form_id)) 
	
	return render_template('user-faculty/peer-eval-pages/user-peer-eval-3.html', evaluated=evaluated, rubric=rubric, form_id=form_id)

@dpsm_eval_blueprint.route('/faculty/peer-eval-page-4<string:evaluated_email><string:form_id>/evaluate/', methods=['GET', 'POST'])
def peer_eval_page_4(evaluated_email, form_id):
	evaluated = user = UserAccounts.query.filter_by(email=evaluated_email).first()
	rubric = questions_peer_eval.query.filter_by(criteria='Attitude towards the support staff')
	
	if request.method == "POST":
		session['peer_eval_10'] = request.form.get('peer_eval_10')
		print(session['peer_eval_10'])
	
		return redirect('/faculty/peer-eval-page-5<string:evaluated_email>/evaluate/', evaluated_email=evaluated_email, form_id=form_id) 
	
	return render_template('user-faculty/peer-eval-pages/user-peer-eval-4.html', evaluated=evaluated, rubric=rubric, form_id=form_id)

@dpsm_eval_blueprint.route('/faculty/peer-eval-page-5<string:evaluated_email><string:form_id>/evaluate/', methods=['GET', 'POST'])
def peer_eval_page_5(evaluated_email, form_id):
	evaluated = user = UserAccounts.query.filter_by(email=evaluated_email).first()
	rubric = questions_peer_eval.query.filter_by(criteria='Attitude towards University policies and regulations.')
	
	if request.method == "POST":
		session['peer_eval_11'] = request.form.get('peer_eval_11')
		print(session['peer_eval_11'])

		
	
	return render_template('user-faculty/peer-eval-pages/user-peer-eval-5.html', evaluated=evaluated, rubric=rubric)

#SELF EVAL PAGES
@dpsm_eval_blueprint.route('/faculty/self-eval-page-1')
def self_eval_page_1():
	user = UserAccounts.query.filter_by(email=session["email"]).first()
	rubric = questions_self_eval.query.filter_by(criteria='Professionalism')
	return render_template('user-faculty/self-eval-pages/user-self-eval-1.html', evaluated=user, rubric=rubric)

@dpsm_eval_blueprint.route('/faculty/self-eval-page-2')
def self_eval_page_2():
	user = UserAccounts.query.filter_by(email=session["email"]).first()
	rubric = questions_self_eval.query.filter_by(criteria='Attitude towards students')
	return render_template('user-faculty/self-eval-pages/user-self-eval-2.html', evaluated=user, rubric=rubric)

@dpsm_eval_blueprint.route('/faculty/self-eval-page-3')
def self_eval_page_3():
	user = UserAccounts.query.filter_by(email=session["email"]).first()
	rubric = questions_self_eval.query.filter_by(criteria='Attitude towards peers')
	return render_template('user-faculty/self-eval-pages/user-self-eval-3.html', evaluated=user, rubric=rubric)

@dpsm_eval_blueprint.route('/faculty/self-eval-page-4')
def self_eval_page_4():
	user = UserAccounts.query.filter_by(email=session["email"]).first()
	rubric = questions_self_eval.query.filter_by(criteria='Attitude towards support and administrative staff')
	return render_template('user-faculty/self-eval-pages/user-self-eval-4.html', evaluated=user, rubric=rubric)

@dpsm_eval_blueprint.route('/faculty/self-eval-page-5')
def self_eval_page_5():
	user = UserAccounts.query.filter_by(email=session["email"]).first()
	rubric = questions_self_eval.query.filter_by(criteria='Attitude towards the profession and administration')
	return render_template('user-faculty/self-eval-pages/user-self-eval-5.html', evaluated=user, rubric=rubric)

###############################################################################################