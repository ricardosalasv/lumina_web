from flask import render_template, flash, redirect, request, url_for, session, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from lumina import app, db, bcrypt, login_manager
from lumina.forms import RegistrationForm, LoginForm, CreateProjectForm, ProjectDataForm
from lumina.models import Users, Projects, Models, Finishes, Arch_Materials, Brands, Floorplan_Shapes
from lumina.helpers import GenerateProjectCode, CalculateProject
import json
from datetime import datetime
import time

@app.route("/")
@app.route("/home")
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

            user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
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

        user = Users.query.filter_by(email=form.email.data).first()

        if not user:
            user = Users.query.filter_by(username=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            print(f"The current user ID is: {user.id}")

            return redirect(next_page) if next_page else redirect(url_for('home'))
        
        else:
            flash(f'Login failed, please check and fill the fields again', 'warning')

    return render_template("login.html", title = "Login", form=form)

@app.route("/project", methods=["GET", "POST", "PUT"])
@login_required
def project():

    # Creating a new instance of the form
    form = ProjectDataForm()

    # Getting the brands and models from the DB
    # and combining them into a JSON to be parsed by JS
    # in order to filter the Models dropdown based on the selected brand
    brands = Brands.query.all()
    models = Models.query.all()

    # Creating dictionary
    brandsModelsJSON = {}

    for brand in list(map(lambda x : x.name, brands)):
        
        # Filtering the models based on the current brand
        modelsByBrand = list(filter(lambda x : x.brand.name == brand, models))
        modelsByBrand = list(map(lambda x : x.serializedForProject, modelsByBrand))

        brandsModelsJSON[brand] = modelsByBrand

    # To execute when the Calculate button is clicked
    if request.method == "PUT":
        
        for key, value in request.form.items():

            if not value:

                return CalculateProject(request.form, returnZero=True)

        return CalculateProject(request.form)
    
    # To execute when the project is created
    if request.method == "POST":

        # But if the project is loaded instead, execute this
        if "projectCode" in request.form.keys():

            projectCode = request.form["projectCode"]
            projectId = request.form["projectId"]

            selectedProject = list(filter(lambda x : x.id == int(projectId) and \
                                                    x.projectCode == projectCode, Projects.query.all()))[0]
            selectedProject = selectedProject.serialized
            selectedProject["LoadedProject"] = True

            return render_template("project.html", title = "Project", project=selectedProject, brandsModelsJSON=brandsModelsJSON, form=form)

        project = session["projectData"]
        project = json.loads(project)

        return render_template("project.html", title = "Project", project=project, brandsModelsJSON=brandsModelsJSON, form=form)
            

@app.route("/newProject", methods=["GET", "POST"])
@login_required
def newProject():

    form = CreateProjectForm()

    if form.validate_on_submit():

        # Creating new project information
        projectName = form.projectName.data
        
        projectCode = GenerateProjectCode(current_user, projectName)

        # Inserting the project into the DB
        project = Projects(
            name=projectName, 
            projectCode=projectCode, 
            user_id=current_user.id, 
            model_id=Models.query.all()[0].id,
            fpShape_id=list(filter(lambda x : x.name == "Rectangular", Floorplan_Shapes.query.all()))[0].id
        )
        db.session.add(project)
        db.session.commit()

        # Getting the recently created project from the DB
        projectFromDB = list(filter(lambda x : x.projectCode == project.projectCode \
                                               and x.id == project.id, Projects.query.all()))[0]

        # Getting a JSON object with all the relevant information to pass to the /project page when the redirection happens
        projectJSON = json.dumps(projectFromDB.serialized)

        session["projectData"] = projectJSON

        return redirect(url_for("project"), code=307)

    return render_template("newProject.html", title = "New Project", form=form)

@app.route("/loadProject", methods=["GET"])
@login_required
def loadProject():

    projects = Projects.query.all()

    # Filtering the projects that belong to the current user
    projects = list(filter(lambda x : x.user_id == current_user.id, projects))
    projects.sort(key=lambda x : x.dateModified, reverse=True)

    return render_template("loadProject.html", title = "Load Project", projects=projects)

@app.route("/catalogue")
@login_required
def catalogue():

    allModels = Models.query.all()
    allModels.sort(key=lambda x : (x.brand.name, x.mark))

    return render_template("catalogue.html", title = "Catalogue", counter=0, models=allModels)

@app.route("/logout")
@login_required
def logout():

    print(f"The user (ID: {current_user.id}) has logged out.")

    logout_user()

    return redirect(url_for('login'))
