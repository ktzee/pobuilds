import os

SECRET_KEY = 'you-will-never-guess'
DEBUG = True
DB_USERNAME = 'ktz'
DB_PASSWORD = ''
DATABASE_NAME = 'pobuilds'
DB_HOST = 'localhost'
DB_URI = 'mysql+pymysql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
