import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'SECRET_KEY'
SQLALCHEMY_DATABASE_URI = 'postgres://is_required!'
SQLALCHEMY_ECHO = False
THIS_IS_THUNDERDOME = True
PAGINATION_SIZE = 20
SECURITY_USER_IDENTITY_ATTRIBUTES = 'username'
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = 'SaltyPirates!! ARRRR'
try:
    from user_config import *
except ImportError:
    pass  # log using defaults.