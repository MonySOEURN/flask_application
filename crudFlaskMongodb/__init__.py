
from flask import Flask
# from flask_mongoalchemy import MongoAlchemy
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from bson.json_util import dumps
# from bson.objectid import ObjectId
# from flask import jsonify, request
# import json
# from werkzeug.security import generate_password_hash, check_password_hash
# from mongoengine import Document
# from mongoengine import DateTimeField, StringField, ReferenceField, ListField
# from datatime import datetime


app = Flask(__name__, template_folder='templates')

# ---- from library pymongo--------
app.config['DEFAULT_CONNECTION_NAME'] = "mongodb://localhost:27017"
app.config['DEFAULT_DATABASE_NAME'] = "Users"

app.config['MONGO_DBNAME'] = 'Users'
app.config['MONGO_URI'] = "mongodb://localhost:27017" 
app.secret_key = "secretkey"
db = PyMongo(app)
login_manager = LoginManager(app)
# ------------

# --------flask-MongoAlchemy------------
# app.config['MONGOALCHEMY_DATABASE'] = 'Users'
# app.config['MONGOALCHEMY_CONNECTION_STRING'] = "mongodb://localhost:27017"
# app.config['SECRET_KEY'] = '81888e25a52b564b37ac50dcc7320a5b'
# db = MongoAlchemy(app)
bcrypt = Bcrypt(app)
# --------------------

from crudFlaskMongodb import routes