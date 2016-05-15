# Import flask dependencies
from flask import Blueprint

# Import the database session from the main app module
from app import session

# Import module models
from app.catalog.models import Category


# Define the blueprint: 'catalogApi', set its url prefix: app.url/catalog
catalogApiBlueprint = Blueprint('catalogApi', __name__, url_prefix='/catalog')


@catalogApiBlueprint.route('/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Catalog=[i.serialize for i in categories])
