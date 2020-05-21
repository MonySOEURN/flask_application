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

