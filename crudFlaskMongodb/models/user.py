from crudFlaskMongodb.models.index import *

@login_manager.user_loader
def load_user(user_id):
    # mistake error of mongoengine.errors.InvalidQueryError: Not a query object: 5ecbda95c6b624c26e55a04b. Did you intend to use key=value?
    # return User.objects(user_id).get_or_404
    # change to below it work 
    return User.objects().get( id = user_id) 

class User(Document, UserMixin):
    username = StringField(max_length=20, required=True, unique=True)
    email = StringField(max_length=120, required=True, unique=True)
    image_file = StringField(max_length=20, required=True, default='default.jpg')
    password = StringField(max_length=60, required=True)
    # post = ListField(Post, required=True)
    created_at = DateTimeField(defaul=datetime.utcnow)
    updated_at = DateTimeField()
    deleted_at = DateTimeField()

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"