
from flask import Flask
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

api_key = '4321fb8efd95be77186b5fca6ca52b23'
base_url = 'https://api.themoviedb.org/3/discover/movie?api_key='+api_key
# base_url = 'https://api.themoviedb.org/3/discover/movie/?api_key'+api_key


# function using for multiple app version such as testing or production
def create_app(config_class = Config):
    app = Flask(__name__, template_folder='templates')
    # app = Flask(__name__)

    # using class Config
    app.config.from_object(Config)

    # expandable extension
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)


    #------------- import to initialize all Blueprin -----------
    from crudFlaskMongodb.errors.handlers import errors
    from crudFlaskMongodb.users.routes import users
    from crudFlaskMongodb.posts.routes import posts
    from crudFlaskMongodb.main.routes import main
    from crudFlaskMongodb.movies.routes import movies

    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(movies)
    #------------------------

    return app
