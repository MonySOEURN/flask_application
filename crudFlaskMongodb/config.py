class Config:

    # flask-mongoengine
    SECRET_KEY = '81888e25a52b564b37ac50dcc7320a5b'
    DEFAULT_CONNECTION_NAME = "mongodb://localhost:27017"
    DEFAULT_DATABASE_NAME = "Users"

    MONGO_DBNAME = 'Users'
    MONGO_URI = "mongodb://localhost:27017" 

    # flask-mail
    MAIL_SERVER ='smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'c813910e8360f8'
    MAIL_PASSWORD = 'e4bc9cadc74800'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # flask-mongoalchemy
    # MONGOALCHEMY_DATABASE = 'Users'
    # MONGOALCHEMY_CONNECTION_STRING  = "mongodb://localhost:27017"
    # SECRET_KEY = '81888e25a52b564b37ac50dcc7320a5b'