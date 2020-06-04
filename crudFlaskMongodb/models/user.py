from crudFlaskMongodb.models.index import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    # mistake error of mongoengine.errors.InvalidQueryError: Not a query object: 5ecbda95c6b624c26e55a04b. Did you intend to use key=value?
    # return User.objects(user_id).get_or_404
    # change to below it work 
    return User.objects().get( id = user_id) 

class User(db.Document, UserMixin):
    username = db.StringField(max_length=20, required=True, unique=True)
    email = db.StringField(max_length=120, required=True, unique=True)
    image_file = db.StringField(max_length=20, required=True, default='default.jpg')
    password = db.StringField(max_length=60, required=True)
    # post = ListField(Post, required=True)
    created_at = db.DateTimeField(defaul=datetime.utcnow)
    updated_at = db.DateTimeField()
    deleted_at = db.DateTimeField()

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        # to get value id of objectId use str(object.id)
        return s.dumps({'user_id': str(self.id)}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.objects().get( id = user_id)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"