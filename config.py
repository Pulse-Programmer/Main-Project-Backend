# Standard library imports
from dotenv import load_dotenv
import os
# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from flasgger import Swagger

# Load environment variables
load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.khqalbapxdbyuuscsdww:w!hSBVH!VF96SR@aws-0-eu-central-1.pooler.supabase.com:6543/postgres' #'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.json.compact = False

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
CORS(app)