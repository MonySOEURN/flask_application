
from flask import Flask, render_template
# from flask_mongoalchemy import MongoAlchemy
# from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from crudFlaskMongodb.config import Config

# ---- from library pymongo or flask_mongoengine --------
db = MongoEngine()
#------------------


# ---------- add and config login manager---------------
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
# ------------

# ----------- add and config mail-------------
mail = Mail()
# ------------

# --------flask-MongoAlchemy------------
# db = MongoAlchemy(app)
bcrypt = Bcrypt()
# --------------------


# function using for multiple app version such as testing or production
def create_app(config_class = Config):
    app = Flask(__name__, template_folder='templates')
    # app = Flask(__name__)

    # expandable extension
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    # using class Config
    app.config.from_object(Config)


    #------------- import to initialize all Blueprin -----------
    from crudFlaskMongodb.errors.handlers import errors
    from crudFlaskMongodb.users.routes import users
    from crudFlaskMongodb.posts.routes import posts
    from crudFlaskMongodb.main.routes import main

    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    #------------------------

    return app
