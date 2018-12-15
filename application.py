import json
import os
import random
import string
from functools import wraps

import google.oauth2.credentials
import google_auth_oauthlib.flow
import httplib2
import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask import session as login_session
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, Item, User

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)


engine = create_engine('sqlite:///itemcatalog.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if login_session.get('gplus_id') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['profile', 'email', 'openid'])

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required.
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, login_session['state'] = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true',
        state=state)
    return redirect(authorization_url)

@app.route('/logout')
def logout():
    if isLoggedIn:
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['access_token']
        flash("You have successfully been logged out.")
        return redirect(url_for('viewCategories'))
    else:
        flash("You were not logged in.")
        return redirect(url_for('viewCategories'))

@app.route('/oauth2callback')
def oauth2callback():
    # check if response was an error
    error = request.args.get('error')
    if error:
        flash("Error Logging In: {}".format(error))
        return redirect(url_for('viewCategories'))

    # Validate state token
    if request.args.get('state') != login_session['state']:
        flash("Error Logging In: {}".format("Invalid State"))
        return redirect(url_for('viewCategories'))

    # Obtain authorization code
    code = request.args.get('code')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = url_for('oauth2callback', _external=True)
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        flash("Error Logging In: {}".format(
            "Failed to upgrade the authorization code."))
        return redirect(url_for('viewCategories'))

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        flash("Error Logging In: {}".format(result.get('error')))
        return redirect(url_for('viewCategories'))

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        flash("Error Logging In: {}".format(
            "Token's user ID doesn't match given user ID."))
        return redirect(url_for('viewCategories'))

    # Verify that the access token is valid for this app.
    CLIENT_ID = json.loads(open('client_secret.json', 'r').read())[
        'web']['client_id']
    if result['issued_to'] != CLIENT_ID:
        flash("Error Logging In: {}".format(
            "Token's client ID does not match app's."))
        return redirect(url_for('viewCategories'))

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        flash("Error Logging In: {}".format(
            'Current user is already connected.'))
        return redirect(url_for('viewCategories'))

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        flash('New user {} added'.format(login_session['username']))
    login_session['user_id'] = user_id

    flash("you are now logged in as {}".format(login_session['username']))
    return redirect(url_for('viewCategories'))

def isLoggedIn():
    if login_session.get('gplus_id') is None:
        return False
    return True

def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   google_id=login_session['gplus_id'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/')
@app.route('/ItemCatalog')
def viewCategories():
    categories = session.query(Category).all()
    if not isLoggedIn():
        flash("Log in to Add, Edit, or Delete Your Own Categories")
    return render_template('categoryView.html', categories=categories, isLoggedIn=isLoggedIn())


@app.route('/ItemCatalog/Categories/Add', methods=['GET', 'POST'])
@login_required
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


@app.route('/ItemCatalog/Categories/<int:categoryID>/Edit', methods=['GET', 'POST'])
@login_required
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


@app.route('/ItemCatalog/Categories/<int:categoryID>/Delete', methods=['GET', 'POST'])
@login_required
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
    if not isLoggedIn():
        flash("Log in to Add, Edit, or Delete Your Own Items")
    return render_template('itemView.html', category=category, items=items, isLoggedIn=isLoggedIn())


@app.route('/ItemCatalog/Categories/<int:categoryID>/Items/Add', methods=['GET', 'POST'])
@login_required
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


@app.route('/ItemCatalog/Items/<int:itemID>/Edit', methods=['GET', 'POST'])
@login_required
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


@app.route('/ItemCatalog/Items/<int:itemID>/Delete', methods=['GET', 'POST'])
@login_required
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
@login_required
def jsonifyAll():
    pass
    return 'json of all categories and items'


if(__name__ == '__main__'):
    app.config.update({
        'SECRET_KEY': 'asd098wer',
        'DEBUG': True,
    })
    app.run(host='0.0.0.0', port=8000)
