# Standard library imports

import os
from dotenv import load_dotenv
# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from flasgger import Swagger
from flask_mail import Mail, Message 
# from sqlalchemy import create_engine


# Load environment variables
load_dotenv()

# ssl_args = {
#     'sslmode': 'require',
#     'sslcert': os.environ.get('SSL_CERT')
# }

# Construct the SQLAlchemy database URI
# db_uri = os.environ.get('DATABASE_URI')

# # Combine URI with SSL parameters
# engine = create_engine(db_uri, connect_args=ssl_args)

app = Flask(__name__)
swagger = Swagger(app)
#session cookies configuration
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

#configuration for flask mailman
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "edwardmwangi94@gmail.com"  #Your email address
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')  #Your email password
app.config['MAIL_USE_TLS'] = True  # Use TLS
app.config['MAIL_USE_SSL'] = False   #Not using SSL
app.config['MAIL_DEFAULT_SENDER'] = "edwardmwangi94@gmail.com"  # Default sender
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)



app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')#os.getenv('DATABASE_URI') #'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.json.compact = False

# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     "connect_args": {
#     'sslmode': 'require',
#     'sslcert': os.environ.get('SSL_CERT')
# }
# }

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate bcrypt
bcrypt = Bcrypt(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app, supports_credentials=True)