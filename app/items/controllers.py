# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, redirect, url_for, session as login_session

# Import the database session from the main app module
from app import session

from sqlalchemy import asc

# Import module models
from app.catalog.models import Category
from app.items.models import Item

# Define the blueprint: 'item', set its url prefix: app.url/catalog
itemBlueprint = Blueprint('item', __name__, url_prefix='/catalog')


# Set the route and accepted methods
@itemBlueprint.route('/item/<int:item_id>/show', methods=['GET'])
def showItem(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('items/item.html', item=item)


@itemBlueprint.route('/newItem', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect(url_for('auth.showLogin'))
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['category_id']:
            newItem = Item(name=request.form['name'],
                           description=request.form['description'],
                           category_id=request.form['category_id'])
            session.add(newItem)
            session.commit()
            flash('New Item %s Successfully Created' % (newItem.name))
            return redirect(url_for('catalog.showCatalog'))
        else:
            flash('All fields are mandatory')
            return render_template('items/newitem.html', categories=categories)
    else:
        return render_template('items/newitem.html', categories=categories)


@itemBlueprint.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect(url_for('auth.showLogin'))
    categories = session.query(Category).order_by(asc(Category.name))
    editedItem = session.query(Item).filter_by(id=item_id).one()

    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['category_id']:
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
            editedItem.category_id = request.form['category_id']
            session.add(editedItem)
            session.commit()
            flash('Item Successfully Edited')
            return redirect(url_for('catalog.showCatalog'))
        else:
            flash('All fields are mandatory')
            return render_template('items/edititem.html', item=editedItem, categories=categories)
    else:
        return render_template('items/edititem.html', item=editedItem, categories=categories)


@itemBlueprint.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect(url_for('auth.showLogin'))
    itemToDelete = session.query(Item).filter_by(id=item_id).one()

    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this item. Please create your own item in order to delete.');}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('catalog.showCatalog'))
    else:
        return render_template('items/deleteitem.html', item=itemToDelete)
