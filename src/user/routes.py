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
from .models import Evaluation, UserAccounts, to_evaluate, questions_peer_eval
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
	return render_template('user-faculty/dashboard.html')

@dpsm_eval_blueprint.route('/faculty_list')
#@login_required
def faculty_list():
	user = UserAccounts.query.filter_by(email=session["email"]).first()
	evaluated = user.is_evaluated_email
	need_to_be_evaluated = to_evaluate.query.all()
	
	return render_template('user-faculty/user-faculty-list.html', evaluated=evaluated, not_evaluated=need_to_be_evaluated)

###############################################################################################
#USER TEMPLATES

#PEER EVAL PAGES
@dpsm_eval_blueprint.route('/faculty/peer-eval-page-1<string:evaluated_email>/evaluate/', methods=['GET', 'POST'])
def peer_eval_page_1(evaluated_email):
	evaluated = user = UserAccounts.query.filter_by(email=evaluated_email).first()
	rubric = questions_peer_eval.query.filter_by(criteria='Professionalism and work ethics')
	return render_template('user-faculty/peer-eval-pages/user-peer-eval-1.html', evaluated=evaluated, rubric=rubric)

@dpsm_eval_blueprint.route('/faculty/peer-eval-page-2')
def peer_eval_page_2():
	return render_template('user-faculty/peer-eval-pages/user-peer-eval-2.html')

@dpsm_eval_blueprint.route('/faculty/peer-eval-page-3')
def peer_eval_page_3():
	return render_template('user-faculty/peer-eval-pages/user-peer-eval-3.html')

@dpsm_eval_blueprint.route('/faculty/peer-eval-page-4')
def peer_eval_page_4():
	return render_template('user-faculty/peer-eval-pages/user-peer-eval-4.html')

@dpsm_eval_blueprint.route('/faculty/peer-eval-page-5')
def peer_eval_page_5():
	return render_template('user-faculty/peer-eval-pages/user-peer-eval-5.html')

#SELF EVAL PAGES
@dpsm_eval_blueprint.route('/faculty/self-eval-page-1')
def self_eval_page_1():
	return render_template('user-faculty/self-eval-pages/user-self-eval-1.html')

@dpsm_eval_blueprint.route('/faculty/self-eval-page-2')
def self_eval_page_2():
	return render_template('user-faculty/self-eval-pages/user-self-eval-2.html')

@dpsm_eval_blueprint.route('/faculty/self-eval-page-3')
def self_eval_page_3():
	return render_template('user-faculty/self-eval-pages/user-self-eval-3.html')

@dpsm_eval_blueprint.route('/faculty/self-eval-page-4')
def self_eval_page_4():
	return render_template('user-faculty/self-eval-pages/user-self-eval-4.html')

@dpsm_eval_blueprint.route('/faculty/self-eval-page-5')
def self_eval_page_5():
	return render_template('user-faculty/self-eval-pages/user-self-eval-5.html')

###############################################################################################

#ADMIN TEMPLATES
@dpsm_eval_blueprint.route('/admin-dashboard')
def admin_dashboard():
	active_forms = []
	data = mongo.db.evaluation.find({"is_active" : True})
	
	for document in data:
		#print(document)
		
		active_forms.append(document)

	print(active_forms)
	return render_template('admin/dashboard.html', forms = active_forms )

@dpsm_eval_blueprint.route('/admin/user-list')
def admin_user_list():
	user_list = UserAccounts.query.all()
	return render_template('admin/user/user-list.html', users = user_list)

@dpsm_eval_blueprint.route('/admin/add-user', methods=['GET', 'POST'])
def add_user():

	email = request.form.get('email')
	first_name = request.form.get('first_name')
	middle_name = request.form.get('middle_name')
	last_name = request.form.get('last_name')
	unit = request.form.get('unit')
	status = request.form.get('status')
	position1 = request.form.get('position1')
	position2 = request.form.get('position2')
	position3 = request.form.get('position3')
	work_title = request.form.get('work_title')

	
	if position1 == 'True':
		is_unit_head = True
	else:
		is_unit_head = False

	if position2 == 'True':
		is_unit_apc = True
	else:
		is_unit_apc = False

	if position3 == 'True':
		is_dept_head = True
	else:
		is_dept_head = False
	
	
	user = UserAccounts.query.filter_by(email=email).first()

	if user:
		# If user exists then handle here.
		flash('User already exists.')
		return redirect(url_for('dpsm_eval_blueprint.add_user'))
	
	# New User ID
	new_id = UserAccounts.query.order_by(UserAccounts.id.desc()).first()
	eval_email = []
	eval_email.append(email)
	if request.method == 'POST':
		new_user = UserAccounts(id = new_id.id + 1,email=email, first_name=first_name,
		middle_name=middle_name,
		last_name=last_name,
		is_unit_head=is_unit_head,
		is_unit_apc = is_unit_apc,
		is_dept_head=is_dept_head,
		status=status,
		work_title=work_title, 
		unit = unit,
		is_evaluated_email = eval_email)
		
		user_reference = {
			"_id" : uuid.uuid4().hex,
			"email": request.form.get('email'),
		}
		mongo.db.users.insert_one(user_reference)
		db.session.add(new_user)
		db.session.commit()


		return redirect(url_for('dpsm_eval_blueprint.admin_user_list'))

	return render_template('admin/user/add-user.html')

@dpsm_eval_blueprint.route('/admin/delete/<int:id>')
def delete_user(id):
	user = UserAccounts.query.get(id)

	try:
		db.session.delete(user)
		db.session.commit()
		
		return redirect(url_for('dpsm_eval_blueprint.admin_user_list'))
	except:
		return 'Problem deleting user'

@dpsm_eval_blueprint.route('/admin/add-form')
def open_form():
	return render_template('admin/forms/renewal/open-form.html')

@dpsm_eval_blueprint.route('/renewalAction', methods=['GET', 'POST'])
def open_form_renewal():
	title = request.form.get('title')
	purpose_eval = request.form.get('purpose_eval')
	start_date = request.form.get('start_date')
	end_date = request.form.get('end_date')
	release_date = request.form.get('release_date')

	id = uuid.uuid4().hex
	data = {
		"title": title,
		"purpose_of_evaluation": purpose_eval,
		"start_date": start_date,
		"end_date": end_date,
		"release_date": release_date,
		"is_active": True,
		"is_done": False,
	}
	mongo.db.evaluation.update_one( {"_id": id}, { "$setOnInsert": data}, upsert = True)
	
	
	return jsonify({"success" : "Evaluation added "}), 200

