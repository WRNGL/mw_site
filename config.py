# config.py

import os

# where script runs
# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.dirname(os.path.abspath(__file__))


DATABASE = 'mwstats.db'

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret_is_secret'

# defines full path to database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH