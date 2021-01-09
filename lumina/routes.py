from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from lumina import app, db, bcrypt, login_manager
from lumina.forms import RegistrationForm, LoginForm
from lumina.models import users, projects
from datetime import datetime
import time

@app.route("/")
@login_required
def home():
    return render_template("home.html", title = "Home")

@app.route("/register", methods=['GET', 'POST'])
def register():

    # Redirecting to home if an user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Main code
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

    # Redirecting to home if an user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Main code
    form = LoginForm()

    if form.validate_on_submit():

        user = users.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            print(f"The current user ID is: {user.id}")

            return redirect(next_page) if next_page else redirect(url_for('home'))
        
        else:
            flash(f'Login failed, please check and fill the fields again', 'warning')

    return render_template("login.html", title = "Login", form=form)

@app.route("/project", methods=["GET", "POST"])
@login_required
def project():

    if request.method == "POST":

        return render_template("project.html", title = "Project", variable="POST")
    
    else:

        return render_template("project.html", title = "Project", variable="GET")

    

@app.route("/loadProject")
@login_required
def loadProject():
    return render_template("loadProject.html", title = "Load Project")

@app.route("/catalogue")
@login_required
def catalogue():
    return render_template("catalogue.html", title = "Catalogue")

@app.route("/logout")
@login_required
def logout():

    print(f"The user (ID: {current_user.id}) has logged out.")

    logout_user()

    return redirect(url_for('login'))