from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lumina.models import Users, Arch_Materials, Floorplan_Shapes, Models, Brands

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), 
                                                   Length(min=4, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(),
                                                    Length(min=2, max=20)])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                    EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = Users.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):

        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is already in use.')

class LoginForm(FlaskForm):

    email = StringField('Email or Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(),
                                                    Length(min=2, max=20)])

    remember = BooleanField('Remember me')

    submit = SubmitField('Login')

class CreateProjectForm(FlaskForm):

    projectName = StringField('Project Name', validators=[DataRequired(), Length(min=5, max=20)])

    createProject = SubmitField('Create')

class ProjectDataForm(FlaskForm):

    # Room Dimensions
    roomLength = FloatField("Room Length (m)", validators=[DataRequired()])
    roomWidth = FloatField("Room Width (m)", validators=[DataRequired()])
    roomHeight = FloatField("Room Height (m)", validators=[DataRequired()])
    roomArea = FloatField("Room Area (sqm)", validators=[DataRequired()])

    # Getting the architectural materials from the DB
    archMaterials = Arch_Materials.query.all()
    archMaterials = list(map(lambda x : x.name, archMaterials))
    archMaterials.sort()

    # Materials
    roomCeilingMaterial = SelectField("Ceiling Material", 
                                    validators=[DataRequired()],
                                    choices=archMaterials)

    roomWallMaterial = SelectField("Walls Material",
                                    validators=[DataRequired()],
                                    choices=archMaterials)

    roomFloorMaterial = SelectField("Floor Material",
                                    validators=[DataRequired()],
                                    choices=archMaterials)

    # Getting the brands from the DB
    brands = Brands.query.all()
    brands = list(map(lambda x : x.name, brands))
    brands.sort()

    # Selecting the brand in order to filter the shown models
    brand = SelectField("Fixture Brand", 
                                    validators=[DataRequired()], 
                                    choices=brands)

    # Getting the fixture models from the DB
    fixtureModels = Models.query.all()
    fixtureModels = list(map(lambda x : x.name, fixtureModels))
    fixtureModels.sort()

    # Model of the fixture to use or being used
    fixtureModel = SelectField("Fixture Model", 
                                    validators=[DataRequired()], 
                                    choices=fixtureModels)

    # Shape of the floorplan
    fpShapes = Floorplan_Shapes.query.all()
    fpShapes = list(map(lambda x : x.name, fpShapes))

    floorplanShape = RadioField("Floorplan Shape",
                                validators=[DataRequired()],
                                choices=fpShapes)

    # Lighting plane height
    lightingPlaneHeight = FloatField("Lighting Plane Height", validators=[DataRequired()])

    # Lux requirement specified by the user
    luxRequirement = IntegerField("Room Lux Requirement", validators=[DataRequired()])

    # OUTPUTS
    # Selected fixture's lumens
    fixtureLumens = IntegerField("Fixture's lumens")
    
    # Fixture's finish
    fixtureFinish = StringField("Fixture's Finish")
    
    # Selected fixture's cost
    fixtureCost = FloatField("Fixture's Cost")

    # Calculate button
    calculate = SubmitField('Login')
