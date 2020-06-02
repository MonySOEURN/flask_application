
from flask import Flask, render_template
# from flask_mongoalchemy import MongoAlchemy
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
# app = Flask(__name__)

# ---- from library pymongo--------
app.config['DEFAULT_CONNECTION_NAME'] = "mongodb://localhost:27017"
app.config['DEFAULT_DATABASE_NAME'] = "Users"

app.config['MONGO_DBNAME'] = 'Users'
app.config['MONGO_URI'] = "mongodb://localhost:27017" 
app.secret_key = "secretkey"
db = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# ------------

# --------flask-MongoAlchemy------------
# app.config['MONGOALCHEMY_DATABASE'] = 'Users'
# app.config['MONGOALCHEMY_CONNECTION_STRING'] = "mongodb://localhost:27017"
# app.config['SECRET_KEY'] = '81888e25a52b564b37ac50dcc7320a5b'
# db = MongoAlchemy(app)
bcrypt = Bcrypt(app)
# --------------------

# import all routes
from crudFlaskMongodb.routes import home, post, authenticate, account