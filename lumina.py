from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime
import time

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = '6f6c96a25bbb642d5ce2c822f1a74000'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lumina_db.db'

# Initialize the database
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    projects = db.relationship('projects', backref='User', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, '{self.email}')"

class catalogue(db.Model): # Available lighting fixtures
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(20), unique=True)
    model = db.Column(db.String(20), unique=True)
    finish = db.Column(db.String(40))
    lm = db.Column(db.Integer)
    w = db.Column(db.Integer)
    dimensions = db.Column(db.String(40), default='L x W x H -or- Radius -or- empty')
    temperature = db.Column(db.Integer, default=4000)
    usage = db.Column(db.String(40), default='General')
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, default=4000)

    def __repr__(self):
        return f"""User('{self.mark}, '{self.manufacturer}', '{self.model}', '{self.finish}', 
                        '{self.lm}', '{self.w}', '{self.dimensions}', '{self.temperature}', 
                        '{self.usage}', '{self.quantity}', '{self.price}')"""

class finishes(db.Model): # Available finishes for the fixtures
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    def __repr__(self):
        return f"User('{self.name}')"

class projects(db.Model): # Created projects
    id = db.Column(db.Integer, primary_key=True)

    # Physical space aspects
    name = db.Column(db.String(40))
    fpShape = db.Column(db.String(40))
    roomLenght = db.Column(db.Float)
    roomWidth = db.Column(db.Float)
    roomHeight = db.Column(db.Float)
    roomCeilingMaterial = db.Column(db.String(40))
    roomWallMaterial = db.Column(db.String(40))
    lux = db.Column(db.Integer)

    # Lighting fixture information
    fixtureMark = db.Column(db.String(10))

    dateModified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.name}')"

@app.route("/")
def home():
    return render_template("home.html", title = "Home")

@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if request.method == "POST":

        if form.validate_on_submit():
            flash(f'Account created for {form.username.data}!', 'success')

            time.sleep(2)

            return redirect(url_for('login'))
            
        else:
            flash(f'Registration failed, please fill the fields again', 'warning')

            return render_template("register.html", title = "Register", form=form)

    else:

        return render_template("register.html", title = "Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        return redirect(url_for('home'))
        
    else:
        flash(f'Login failed, please fill the fields again', 'warning')

        return render_template("login.html", title = "Login", form=form)

    return render_template("home.html", title = "Home")

@app.route("/project")
def project():
    return render_template("project.html", title = "Project")

@app.route("/loadProject")
def loadProject():
    return render_template("loadProject.html", title = "Load Project")

@app.route("/catalogue")
def catalogue():
    return render_template("catalogue.html", title = "Catalogue")

@app.route("/logout")
def logout():
    return render_template("logout.html", title = "Logout")