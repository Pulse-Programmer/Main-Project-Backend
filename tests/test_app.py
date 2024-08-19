import os
import pytest
from config import app


def test_flask_config():
    # Check if Flask app is configured for testing
    # assert app.config['TESTING'] is True

    # Check if SQLAlchemy database URI is correctly set
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URI')
    
    # Check if Flask-Mail configuration is correctly set
    assert app.config['MAIL_SERVER'] == 'smtp.googlemail.com'
    assert app.config['MAIL_PORT'] == 587
    assert app.config['MAIL_USERNAME'] == 'edwardmwangi94@gmail.com'
    assert app.config['MAIL_USE_TLS'] is True
    assert app.config['MAIL_USE_SSL'] is False

    # Check if secret key is set
    assert app.secret_key == b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

    # Check if SQLAlchemy track modifications is turned off
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False

    # Check if JSON compact is set to False
    assert app.json.compact is False