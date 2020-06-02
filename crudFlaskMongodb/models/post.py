from crudFlaskMongodb.models.index import *

from crudFlaskMongodb.models.user import User

class Post(Document):
    title = StringField(max_length=100, required=True)
    date_posted = DateTimeField(default = datetime.utcnow)
    content = StringField(max_length=2000, required=True)
    author = ReferenceField(User, required=True)
    user_id = ReferenceField(User, required=True)
    updated_at = DateTimeField()
    deleted_at = DateTimeField()

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"