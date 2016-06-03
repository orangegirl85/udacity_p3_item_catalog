# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, redirect, url_for

# Import the database session from the main app module
from app import session
from sqlalchemy import asc, desc

# Import module models
from app.catalog.models import Category
from app.items.models import Item

# Define the blueprint: 'catalog', set its url prefix: app.url/catalog
catalogBlueprint = Blueprint('catalog', __name__, url_prefix='/catalog')


# Set the route and accepted methods
@catalogBlueprint.route('/', methods=['GET'])
def showCatalog():
    catalog = session.query(Category).order_by(asc(Category.name))
    latestItems = session.query(Item.name, Item.id, Category.name, Category.id).join(Category).order_by(desc(Item.id)).limit(10)

    latest = []
    for (itemName, itemId, categoryName, categoryId) in latestItems:
        latest.append({'item_name':itemName, 'category_name': categoryName, 'item_id':itemId, 'category_id': categoryId})
    return render_template('catalog/catalog.html', catalog=catalog, latest=latest)


@catalogBlueprint.route('/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('catalog.showCatalog'))
    else:
        return render_template('catalog/newcategory.html')


@catalogBlueprint.route('/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        print 'post'
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('catalog.showCatalog'))
    else:
        return render_template('catalog/editcategory.html', category=editedCategory)


@catalogBlueprint.route('/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('catalog.showCatalog', category_id=category_id))
    else:
        return render_template('catalog/deletecategory.html', item=categoryToDelete)


@catalogBlueprint.route('/catalog/<int:category_id>/items')
def showItems(category_id):
    catalog = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items/items.html', catalog=catalog, items=items, category=category)
