from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

#Connect to Database and create database session
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
    return 'Login page'

@app.route('/disconnect')
def disconnect():
    return 'Disconnect'

#JSON APIs to view Catalog Information
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Catalog=[i.serialize for i in categories])

#Show all categories
@app.route('/')
@app.route('/catalog')
def showCatalog():
    catalog = session.query(Category).order_by(asc(Category.name))
    return render_template('catalog.html', catalog=catalog)

@app.route('/category/new', methods = ['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newcategory.html')

@app.route('/catalog/<int:category_id>/edit/', methods = ['GET', 'POST'])
def editCategory(category_id):
  editedCategory = session.query(Category).filter_by(id=category_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedCategory.name = request.form['name']
        flash('Category Successfully Edited %s' % editedCategory.name)
        return redirect(url_for('showCatalog'))
  else:
    return render_template('editcategory.html', category=editedCategory)

@app.route('/catalog/<int:category_id>/delete/', methods = ['GET','POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCatalog', category_id=category_id))
    else:
        return render_template('deletecategory.html', item=categoryToDelete)


@app.route('/catalog/<int:category_id>/items')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items=items, category=category)

#Create a new item
@app.route('/catalog/<int:category_id>/item/new/',methods=['GET','POST'])
def newCategoryItem(category_id):
  if request.method == 'POST':
      newItem = Item(name=request.form['name'],
                    description=request.form['description'],
                    category_id=category_id)
      session.add(newItem)
      session.commit()
      flash('New Item %s Successfully Created' % (newItem.name))
      return redirect(url_for('showItems', category_id=category_id))
  else:
      return render_template('newitem.html', category_id=category_id)

#Edit an item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('edititem.html', category_id=category_id, item_id=item_id, item=editedItem)


#Delete a category item
@app.route('/catalog/<int:category_id>/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemToDelete)


if __name__ == '__main__':
  app.secret_key = 'catalog_items_super_secret_key'
  app.debug = True
  app.run(host='0.0.0.0', port=8000)
