from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"
app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"

mongo = PyMongo(app)

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
    resp = dumps({ 'message': "user retrieved successfully.", 'status': 200, 'data': user})
    return resp

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

if __name__ == "__main__":
    app.run(debug=True)

