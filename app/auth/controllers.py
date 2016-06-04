# Import flask dependencies
from flask import Blueprint, session as login_session, make_response, render_template, request, flash, redirect, url_for
import random, string
from app import session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import os

# Import module models
from app.auth.models import User

auth_dir = os.path.dirname(__file__)
app_dir = os.path.abspath(os.path.join(auth_dir, os.pardir))
config_dir = os.path.abspath(os.path.join(app_dir, os.pardir))

rel_path = "config/client_secret_google.json"
abs_file_path = os.path.join(config_dir, rel_path)

abs_file_path_fb = os.path.join(config_dir, "config/client_secret_facebook.json")

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

GOOGLE_CLIENT_ID = json.loads(open(abs_file_path, 'r').read())['web']['client_id']
FACEBOOK_APP_ID = json.loads(open(abs_file_path_fb, 'r').read())['web']['app_id']


@auth.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(32))
    login_session['state'] = state
    return render_template('auth/login.html', STATE=state, GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID,
                           FACEBOOK_APP_ID=FACEBOOK_APP_ID)


@auth.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        return error_handler('Invalid state parameters', 401)
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets(abs_file_path, scope='', redirect_uri='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return error_handler('Failed to upgrade the authorization code.', 401)
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        return error_handler(result.get('error'), 500)
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return error_handler("Token's user ID doesn't match given user ID.", 401)
    if result['issued_to'] != GOOGLE_CLIENT_ID:
        return error_handler("Token's client ID doesn't match apps's.", 401)

    stored_credentials = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        return error_handler('Current user is already connected.', 200)

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@auth.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        return error_handler('Invalid state parameter.', 401)
    access_token = request.data

    app_id = json.loads(open(abs_file_path_fb, 'r').read())['web']['app_id']
    app_secret = json.loads(open(abs_file_path_fb, 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@auth.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('catalog.showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('catalog.showCatalog'))


@auth.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        return error_handler('Current user not connected.', 401)
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        return error_handler('Successfully disconnected.', 200)


@auth.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    h.request(url, 'DELETE')[1]


def error_handler(message, code):
    response = make_response(json.dumps(message), code)
    response.headers['Content-Type'] = 'application/json'
    return response


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
