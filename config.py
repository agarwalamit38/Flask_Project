import os
from flask_mysqldb import MySQL

#from app import app
class Config(object):
     SECRET_KEY = os.environ.get('SECRET_KEY') or 'Flask Programmer'
     SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/socialmedia'
     SQLALCHEMY_TRACK_MODIFICATIONS = True