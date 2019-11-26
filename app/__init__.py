# This is the main conroller of the app.

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager




app = Flask(__name__)  # creates the instance of the Flask,assigning the package name
app.config.from_object(Config)

engine = create_engine('mysql://root:root@127.0.0.1:3306/socialmedia',connect_args= dict(host='localhost', port=3306))
Session = sessionmaker(bind=engine)
connection = engine.connect()

Base = declarative_base()
login = LoginManager()
login.init_app(app)
login.login_view = 'login'
login.login_message = u"You are not logged in"
login.login_message_category = "info"

# create a Session
#session = Session()

from app import routes   #Registering the view with the controller

