import os

# Host and Port of the application
HOST = '0.0.0.0'
PORT = 8000

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'catalogitems.db')

# Secret key for signing cookies
SECRET_KEY = "catalog_secret"
