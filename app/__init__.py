# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Configurations
app.config.from_object('config')
app.CLIENT_SECRET_JSON = "app/client_secret.json"

# Define the database object which is imported
# by modules and controllers
# Build the database:
# This will create the database file using SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.item_catalog.models import Base

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)

engine = create_engine('sqlite:///itemcatalog.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.item_catalog.controllers import item_catalog

# Register blueprint(s)
app.register_blueprint(item_catalog)
# app.register_blueprint(xyz_module)
# ..
