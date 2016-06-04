# Import flask dependencies
from flask import Blueprint, jsonify

# Import the database session from the main app module
from app import session

# Import module models
from app.catalog.models import Category
from app.items.models import Item

# Define the blueprint: 'catalogApi', set its url prefix: app.url/catalog
catalogApiBlueprint = Blueprint('catalogApi', __name__, url_prefix='/catalog')


@catalogApiBlueprint.route('.json')
def catalogJSON():
    categories = session.query(Category).all()
    dict = {'Category': []}

    for cat in categories:
        cat_dict = cat.serialize
        items_dict = []
        items = session.query(Item).filter_by(category_id=cat.id)
        for item in items:
            items_dict.append(item.serialize)
        cat_dict['Item'] = items_dict
        dict['Category'].append(cat_dict)

    return jsonify(dict)
