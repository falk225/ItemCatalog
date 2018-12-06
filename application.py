from flask import Flask, render_template, request, redirect, url_for
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
def viewCategories():
    categories = session.query(Category).all()
    return render_template('categoryView.html', categories=categories)

@app.route('/ItemCatalog/Categories/Add', methods=['GET','POST'])
def addCategory():
    if request.method == 'GET':
        #return add category form
        return render_template('categoryAdd.html')
    elif request.method == 'POST':
        #add new category
        category = Category(name=request.form['name'])
        session.add(category)
        session.commit()
        return redirect(url_for('viewCategories'))

@app.route('/ItemCatalog/Categories/<int:categoryID>/Edit', methods=['GET','POST'])
def editCategory(categoryID):
    
    category = session.query(Category).filter_by(id=categoryID).one()
    if request.method == 'GET':
        #return edit category form
        return render_template('categoryEdit.html', category=category)
    elif request.method == 'POST':
        #update category with user input
        category.name = request.form['name']
        session.add(category)
        session.commit()
        return redirect(url_for('viewCategories'))

@app.route('/ItemCatalog/Categories/<int:categoryID>/Delete', methods=['GET','POST'])
def deleteCategory(categoryID):
    category = session.query(Category).filter_by(id=categoryID).one()
    if request.method == 'GET':
        #return confirm delete form
        return render_template('categoryDelete.html', category=category)
    elif request.method == 'POST':
        #delete category from databaes
        session.delete(category)
        session.commit()
        return redirect(url_for('viewCategories'))

@app.route('/ItemCatalog/Categories/<int:categoryID>/Items/View')
def viewItem(categoryID):
    category = session.query(Category).filter_by(id=categoryID).one()
    items = session.query(Item).filter_by(category_id=categoryID).all()
    return render_template('itemView.html', category=category, items=items)

@app.route('/ItemCatalog/Categories/<int:categoryID>/Items/Add', methods=['GET','POST'])
def addItem(categoryID):
    if request.method == 'GET':
        category = session.query(Category).filter_by(id=categoryID).one()
        #return new item form
        return render_template('itemAdd.html', category=category)
    elif request.method == 'POST':
        #add new item
        item = Item(name=request.form['name'])
        item.description = request.form['description']
        item.category_id = categoryID
        session.add(item)
        session.commit()
        return redirect(url_for('viewItem', categoryID=categoryID))

@app.route('/ItemCatalog/Items/<int:itemID>/Edit', methods=['GET','POST'])
def editItem(itemID):
    item = session.query(Item).filter_by(id=itemID).one()
    if request.method == 'GET':
        #return edit item form
        return render_template('itemEdit.html', item=item)
    elif request.method == 'POST':
        #make changes to item from user input
        item.name = request.form['name']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        return redirect(url_for('viewItem', categoryID=item.category_id))

@app.route('/ItemCatalog/Items/<int:itemID>/Delete', methods=['GET','POST'])
def deleteItem(itemID):
    item = session.query(Item).filter_by(id=itemID).one()
    if request.method == 'GET':
        #return confirm deletion page
        return render_template('itemDelete.html', item=item)
    elif request.method == 'POST':
        category_id = item.category_id
        #remove item from database
        session.delete(item)
        session.commit()
        return redirect(url_for('viewItem', categoryID=category_id))

@app.route('/ItemCatalog/api')
def jsonifyAll():
    pass
    return 'json of all categories and items'
    

if(__name__ == '__main__'):
    app.secret_key = 'asd098wer'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)