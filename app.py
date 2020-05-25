from flask import Flask, render_template, url_for, flash, redirect
# from flask_pymongo import PyMongo
from flask.ext.mongoalchemy import MongoAlchemy
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import json
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField
from datatime import datetime

from forms import RegistrationForm, LoginForm

app = Flask(__name__, template_folder='templates')

# ---- from library pymongo--------
# app.config['MONGO_URI'] = "mongodb://localhost:27017/Users" 
# app.secret_key = "secretkey"
# mongo = PyMongo(app)
# ------------

# --------flask-MongoAlchemy------------
app.config['MONGOALCHEMY_DATABASE'] = 'library'
app.config['SECRET_KEY'] = '81888e25a52b564b37ac50dcc7320a5b'
db = MongoAlchemy(app)
# --------------------

# ---------------- New data creation --------------------------

class User(Document):
    name = StringField(max_length=20, required=True, unique=True)
    email = StringField(max_length=120, required=True, unique=True)
    image_file = StringField(max_length=20, required=True, default='default.jpg')
    password = StringField(max_length=60, required=True)
    # post = ListField(Post, required=True)
    created_at = DateTimeField(defaul=datetime.utcnow)
    updated_at = DateTimeField()
    deleted_at = DateTimeField()

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(Document):
    title = StringField(max_length=100, required=True)
    date_posted = DateTimeField(default = datetime.utcnow)
    content = StringField(max_length=2000, required=True)
    user_id = ReferenceField(User, required=True)
    updated_at = DateTimeField()
    deleted_at = DateTimeField()

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

# ------------------------------------------


"""

# ------------CRUD using Flask-PyMongo------------------

# create new user account
@app.route('/add', methods = ['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)

        id = mongo.db.users.insert({
            'name' : _name,
            'email' : _email,
            'pwd' : _hashed_password
        })
        resp = jsonify("user added successfully")

        resp.status_code = 200
        return resp
    else :
        return not_found()

# recieve all user account
@app.route('/users')
def users():
    users = mongo.db.users.find()
    resp = dumps({ 'message': "users retrieved successfully.", 'status': 200, 'data': users})

    return resp

# find specific user accound using id\
@app.route('/users/<id>')
def user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user is not None:
        resp = dumps({ 'message': "user retrieved successfully.", 'status': 200, 'data': user})
        return resp
    else :
        return user_notFound()

# delete user account
@app.route('/users/delete/<id>', methods = ['DELETE'])
def user_delete(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    resp = jsonify({
        'message': "user delete successfully.",
        'status': 200
    })
    resp.status_code = 200
    return resp

@app.route('/users/update/<id>', methods = ['PUT'])
def user_update(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        mongo.db.users.update_one({
                '_id': ObjectId(_id['$oid'])
                if '$oid' in _id else ObjectId(_id)
            },
            {
                '$set': {
                    'name' : _name,
                    'email' : _email,
                    'pwd' : _hashed_password
                }
            }
        )
        resp = jsonify({
            'message': "user update successfully.",
            'status': 200
        })
        resp.status_code = 200
        return resp
    else :
        return user_notFound()

# -------------------- another source part ----------------------------
posts = [
    {
        'author': 'SOEURN Mony',
        'title': 'Blog post 1',
        'content': 'First Post content',
        'date_posted': 'May 22, 2020',
    },
    {
        'author': 'FOUR Year',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'May 23, 2020',
    },
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title= 'Register', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have logged In!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title= 'Login', form=form)


# ------------------------------------------------

# error url response
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url 
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

def user_notFound(error=None):
    message = {
        'message': "user not found",
        'status': 404
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(debug=True)

"""