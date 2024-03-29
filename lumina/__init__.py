from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = os.getenv('LUMINA_DB_SK')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lumina_db.db'

# Initialize the database
db = SQLAlchemy(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from lumina import routes