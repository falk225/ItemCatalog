from flask import Flask, render_template

app = Flask(__name__)

@app.route('/ItemCatalog')
def viewAll():
    return 'main page'

@app.route('/ItemCatalog/Categories/Add', methods=['GET','POST'])
def addCategory():
    return 'new'

@app.route('/ItemCatalog/Categories/<int:categoryID>/Edit', methods=['GET','PUT'])
def editCategory(categoryID):
    return None

@app.route('/ItemCatalog/Categories/<int:categoryID>/Delete', methods=['GET','DELETE'])
def deleteCategory(categoryID):
    return None

@app.route('/ItemCatalog/Categories/<int:categoryID>/Items/Add', methods=['GET','POST'])
def addItem(categoryID):
    pass
    return None

@app.route('/ItemCatalog/Items/<int:itemID>/Edit', methods=['GET','PUT'])
def editItem(itemID):
    pass
    return None

@app.route('/ItemCatalog/Items/<int:itemID>/Delete', methods=['GET','DELETE'])
def deleteItem(itemID):
    pass
    return None

@app.route('/ItemCatalog/api')
def jsonifyAll():
    pass
    return None
    

if(__name__ == '__main__'):
    app.secret_key = 'asd098wer'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)