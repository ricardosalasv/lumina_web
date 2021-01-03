from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = '6f6c96a25bbb642d5ce2c822f1a74000'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lumina_db.db'

# Initialize the database
db = SQLAlchemy(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

from lumina import routes