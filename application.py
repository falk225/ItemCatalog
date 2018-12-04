from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/ItemCatalog')
def viewAll():
    return 'Viewing all categories and items'

@app.route('/ItemCatalog/Categories/Add', methods=['GET','POST'])
def addCategory():
    if request.method == 'GET':
        #return add category form
        pass
    elif request.method == 'POST':
        #add new category
        pass
    return 'Adding a new category'

@app.route('/ItemCatalog/Categories/<int:categoryID>/Edit', methods=['GET','PUT'])
def editCategory(categoryID):
    if request.method == 'GET':
        #return edit category form
        pass
    elif request.method == 'PUT':
        #update category with user input
        pass
    return 'Editing a category {}'.format(categoryID)

@app.route('/ItemCatalog/Categories/<int:categoryID>/Delete', methods=['GET','DELETE'])
def deleteCategory(categoryID):
    if request.method == 'GET':
        #return confirm delete form
        pass
    elif request.method == 'POST':
        #delete category from databaes
        pass
    return 'Deleting a category {}'.format(categoryID)

@app.route('/ItemCatalog/Categories/<int:categoryID>/Items/Add', methods=['GET','POST'])
def addItem(categoryID):
    if request.method == 'GET':
        #return new item form
        pass
    elif request.method == 'POST':
        #add new item
        pass
    return 'Adding a new item to category {}'.format(categoryID)

@app.route('/ItemCatalog/Items/<int:itemID>/Edit', methods=['GET','PUT'])
def editItem(itemID):
    if request.method == 'GET':
        #return edit item form
        pass
    elif request.method == 'PUT':
        #make changes to item from user input
        pass
    return 'Editing item {}'.format(itemID)

@app.route('/ItemCatalog/Items/<int:itemID>/Delete', methods=['GET','DELETE'])
def deleteItem(itemID):
    if request.method == 'GET':
        #return confirm deletion page
        pass
    elif request.method == 'DELETE':
        #remove item from database
        pass
    return 'Deleting item {}'.format(itemID)

@app.route('/ItemCatalog/api')
def jsonifyAll():
    pass
    return 'json of all categories and items'
    

if(__name__ == '__main__'):
    app.secret_key = 'asd098wer'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)