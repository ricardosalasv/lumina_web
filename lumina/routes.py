from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user
from lumina import app, db, bcrypt, login_manager
from lumina.forms import RegistrationForm, LoginForm
from lumina.models import users, projects
from datetime import datetime
import time

@app.route("/")
def home():
    return render_template("home.html", title = "Home")

@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if request.method == "POST":

        if form.validate_on_submit():

            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            user = users(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()

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

        user = users.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            print(f"The current user ID is: {user.id}")

            return redirect(url_for('home'))
        
        else:
            flash(f'Login failed, please check and fill the fields again', 'warning')

    return render_template("login.html", title = "Login", form=form)

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