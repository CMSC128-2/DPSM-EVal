from flask import Blueprint, render_template, session, redirect, abort, request, url_for
from pyasn1.type.univ import Null
import requests
import flask
from flask.globals import request
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from google import auth
import google
from google.auth import credentials
from werkzeug.utils import cached_property
from .models import UserAccounts, to_evaluate
from src import login_manager
from google_auth_oauthlib.flow import Flow
import google.oauth2.id_token as id_token
import os
import pip._vendor.cachecontrol as cacheControl

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
	#email = id_info.get("email")
	
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
	evaluated = user.is_evaluated_id
	need_to_be_evaluated = to_evaluate.query.all()
	need_to_be_evaluated_names = []
	need_to_be_evaluated_pos = []
	evaluated_names = []

	for j in need_to_be_evaluated:
		if j.to_eval_id in evaluated:
			evaluated_names.append(build_name(j.to_eval_first_name, j.to_eval_middle_name, j.to_eval_last_name))

	for j in need_to_be_evaluated:
		need_to_be_evaluated_names.append(build_name(j.to_eval_first_name, j.to_eval_middle_name, j.to_eval_last_name))
		need_to_be_evaluated_pos.append(j.to_eval_position)

	return render_template('user-faculty/user-faculty-list.html', evaluated=evaluated_names, not_evaluated= zip(need_to_be_evaluated_names,need_to_be_evaluated_pos))

@dpsm_eval_blueprint.route('/admin-dashboard')
def about():
	return render_template('admin/dashboard.html')


def build_name(first_name, middle_name, last_name):
	name = ''
	name += first_name
	name += ' ' + middle_name
	name += ' ' + last_name
	return name

@dpsm_eval_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dpsm_eval_blueprint.index'))

