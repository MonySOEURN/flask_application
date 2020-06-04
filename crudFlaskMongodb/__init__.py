
from flask import Flask, render_template
# from flask_mongoalchemy import MongoAlchemy
# from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__, template_folder='templates')
# app = Flask(__name__)

# ---- from library pymongo or flask_mongoengine --------
app.config['DEFAULT_CONNECTION_NAME'] = "mongodb://localhost:27017"
app.config['DEFAULT_DATABASE_NAME'] = "Users"

app.config['MONGO_DBNAME'] = 'Users'
app.config['MONGO_URI'] = "mongodb://localhost:27017" 
app.secret_key = "secretkey"
db = MongoEngine(app)
#------------------


# ---------- add and config login manager---------------
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
# ------------

# ----------- add and config mail-------------
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'c813910e8360f8'
app.config['MAIL_PASSWORD'] = 'e4bc9cadc74800'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
# ------------

# --------flask-MongoAlchemy------------
# app.config['MONGOALCHEMY_DATABASE'] = 'Users'
# app.config['MONGOALCHEMY_CONNECTION_STRING'] = "mongodb://localhost:27017"
# app.config['SECRET_KEY'] = '81888e25a52b564b37ac50dcc7320a5b'
# db = MongoAlchemy(app)
bcrypt = Bcrypt(app)
# --------------------

#------------- import to initialize all routes -----------
from crudFlaskMongodb.errors.handlers import errors
from crudFlaskMongodb.users.routes import users
from crudFlaskMongodb.posts.routes import posts
from crudFlaskMongodb.main.routes import main

app.register_blueprint(errors)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
#------------------------
