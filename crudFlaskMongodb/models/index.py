from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField, DEFAULT_CONNECTION_NAME, register_connection
from datetime import datetime
from crudFlaskMongodb import login_manager
from flask_login import UserMixin

from crudFlaskMongodb import db

register_connection(alias=DEFAULT_CONNECTION_NAME, name='Users')
