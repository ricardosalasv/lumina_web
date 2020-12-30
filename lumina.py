from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html", title = "Home")

@app.route("/register")
def register():
    return render_template("register.html", title = "Register")

@app.route("/login")
def login():
    return render_template("login.html", title = "Login")

@app.route("/project")
def project():
    return render_template("project.html", title = "Project")

@app.route("/loadProject")
def loadProject():
    pass
    return render_template("loadProject.html", title = "Load Project")

@app.route("/catalogue")
def catalogue():
    return render_template("catalogue.html", title = "Catalogue")