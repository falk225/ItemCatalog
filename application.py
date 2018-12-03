from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/ItemCatalog')
def viewAll():
    return 'Viewing all categories and items'

@app.route('/ItemCatalog/Categories/Add', methods=['GET','POST'])
def addCategory():
    return 'Adding a new category'

@app.route('/ItemCatalog/Categories/<int:categoryID>/Edit', methods=['GET','PUT'])
def editCategory(categoryID):
    return 'Editing a category {}'.format(categoryID)

@app.route('/ItemCatalog/Categories/<int:categoryID>/Delete', methods=['GET','DELETE'])
def deleteCategory(categoryID):
    return 'Deleting a category {}'.format(categoryID)

@app.route('/ItemCatalog/Categories/<int:categoryID>/Items/Add', methods=['GET','POST'])
def addItem(categoryID):
    pass
    return 'Adding a new item to category {}'.format(categoryID)

@app.route('/ItemCatalog/Items/<int:itemID>/Edit', methods=['GET','PUT'])
def editItem(itemID):
    pass
    return 'Editing item {}'.format(itemID)

@app.route('/ItemCatalog/Items/<int:itemID>/Delete', methods=['GET','DELETE'])
def deleteItem(itemID):
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