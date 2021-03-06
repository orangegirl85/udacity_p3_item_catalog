# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, redirect, url_for, session as login_session

# Import the database session from the main app module
from app import session, app
from sqlalchemy import asc, desc

# Import module models
from app.catalog.models import Category
from app.items.models import Item

# Define the blueprint: 'catalog', set its url prefix: app.url/catalog
catalogBlueprint = Blueprint('catalog', __name__, url_prefix='/catalog')


# Set the route and accepted methods
@app.route('/', methods=['GET'])
@catalogBlueprint.route('/', methods=['GET'])
def showCatalog():
    catalog = session.query(Category).order_by(asc(Category.name))
    latestItems = session.query(Item.name, Item.id, Category.name, Category.id).join(Category).order_by(
        desc(Item.id)).limit(10)

    latest = []
    for (itemName, itemId, categoryName, categoryId) in latestItems:
        latest.append(
            {'item_name': itemName, 'category_name': categoryName, 'item_id': itemId, 'category_id': categoryId})
    return render_template('catalog/catalog.html', catalog=catalog, latest=latest)


@catalogBlueprint.route('/newCategory', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect(url_for('auth.showLogin'))
    if request.method == 'POST':
        if request.form['name']:
            newCategory = Category(name=request.form['name'], user_id=login_session['user_id'])
            session.add(newCategory)
            flash('New Category %s Successfully Created' % newCategory.name)
            session.commit()
            return redirect(url_for('catalog.showCatalog'))
        else:
            flash('Name is mandatory')
            return render_template('catalog/newcategory.html')
    else:
        return render_template('catalog/newcategory.html')


@catalogBlueprint.route('/<category_name>/edit', methods=['GET', 'POST'])
def editCategory(category_name):
    if 'username' not in login_session:
        return redirect(url_for('auth.showLogin'))
    editedCategory = session.query(Category).filter_by(name=category_name).one()
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this category. Please create your own category in order to edit.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('catalog.showCatalog'))
        else:
            flash('Name is mandatory')
            return render_template('catalog/editcategory.html', category=editedCategory)
    else:
        return render_template('catalog/editcategory.html', category=editedCategory)


@catalogBlueprint.route('/<category_name>/delete', methods=['GET', 'POST'])
def deleteCategory(category_name):
    if 'username' not in login_session:
        return redirect(url_for('auth.showLogin'))
    categoryToDelete = session.query(Category).filter_by(name=category_name).one()
    print categoryToDelete.user_id
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this category. Please create your own category in order to delete.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('catalog.showCatalog'))
    else:
        return render_template('catalog/deletecategory.html', item=categoryToDelete)


@catalogBlueprint.route('/<category_name>/items')
def showItems(category_name):
    catalog = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('items/items.html', catalog=catalog, items=items, category=category)


@catalogBlueprint.route('/<category_name>/<item_name>', methods=['GET'])
def showItem(category_name, item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    return render_template('items/item.html', item=item)
