# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, redirect, url_for

# Import the database session from the main app module
from app import session

# Import module models
from app.items.models import Item

# Define the blueprint: 'item', set its url prefix: app.url/catalog/category_id/item
itemBlueprint = Blueprint('item', __name__, url_prefix='/catalog/<int:category_id>/item')


# Set the route and accepted methods
@itemBlueprint.route('/new', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       category_id=category_id)
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Created' % (newItem.name))
        return redirect(url_for('catalog.showItems', category_id=category_id))
    else:
        return render_template('items/newitem.html', category_id=category_id)


@itemBlueprint.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Category Item Successfully Edited')
        return redirect(url_for('catalog.showItems', category_id=category_id))
    else:
        return render_template('items/edititem.html', category_id=category_id, item_id=item_id, item=editedItem)


@itemBlueprint.route('/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('catalog.showItems', category_id=category_id))
    else:
        return render_template('items/deleteitem.html', item=itemToDelete)
