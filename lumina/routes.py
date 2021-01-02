from flask import render_template, flash, redirect, request, url_for
from lumina import app
from lumina.forms import RegistrationForm, LoginForm
from lumina.models import users, projects

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