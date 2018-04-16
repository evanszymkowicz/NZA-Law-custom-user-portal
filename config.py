import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECURITY_REGISTERABLE = True # user default forms shipped with flask-security
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = b"xxx"
    SECRET_KEY = os.environ.get('SECRETY_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:po_admin@localhost:5433/nza_law'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_POST_LOGIN_VIEW = '/profile/user'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
