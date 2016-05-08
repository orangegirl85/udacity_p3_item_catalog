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

@app.route('/category/new')
def newCategory():
    return "New Category"

@app.route('/category/<int:category_id>/items')
def showItems(category_id):
    return "Item for Category %s" % category_id



if __name__ == '__main__':
  app.secret_key = 'catalog_items_super_secret_key'
  app.debug = True
  app.run(host='0.0.0.0', port=8000)
