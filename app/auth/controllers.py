# Import flask dependencies
from flask import Blueprint

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login')
def showLogin():
    return 'Login page'


@auth.route('/disconnect')
def disconnect():
    return 'Disconnect'
