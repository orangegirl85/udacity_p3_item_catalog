# Import flask and template operators
from flask import Flask, render_template, request, session as app_session, abort
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


#Connect to Database and create database session
Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = app_session.pop('_csrf_token', None)
        tokenFormOrAuth = request.form.get('_csrf_token')
        if not tokenFormOrAuth:
            tokenFormOrAuth = request.args.get('_csrf_token')
        if not token or token != tokenFormOrAuth:
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in app_session:
        app_session['_csrf_token'] = app.config['CSRF_SESSION_KEY']
    return app_session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

# Import a module / component using its blueprint handler variable
from auth.controllers import auth as auth_module
from catalog.controllers import catalogBlueprint as catalog_module
from items.controllers import itemBlueprint as item_module

from catalog.api import catalogApiBlueprint as catalog_api_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(catalog_module)
app.register_blueprint(item_module)

# Register blueprint(s) Api(s)
app.register_blueprint(catalog_api_module)

# Build the database:
# This will create the database file using SQLAlchemy
Base.metadata.create_all(engine)