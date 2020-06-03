from crudFlaskMongodb.models.index import *

from crudFlaskMongodb.models.user import User

class Post(db.Document):
    title = db.StringField(max_length=100, required=True)
    date_posted = db.DateTimeField(default = datetime.utcnow)
    content = db.StringField(max_length=2000, required=True)
    author = db.ReferenceField(User, required=True)
    user_id = db.ReferenceField(User, required=True)
    updated_at = db.DateTimeField()
    deleted_at = db.DateTimeField()

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"