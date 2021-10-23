from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lumina.models import Users, Arch_Materials

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

    roomLength = FloatField("Room Length", validators=[DataRequired()])
    roomWidth = FloatField("Room Width", validators=[DataRequired()])
    roomHeight = FloatField("Room Height", validators=[DataRequired()])
    roomArea = FloatField("Room Area", validators=[DataRequired()])

    # Getting the architectural materials from the DB
    archMaterials = Arch_Materials.query.all()

    roomCeilingMaterial = SelectField("Ceiling Material", 
                                    validators=[DataRequired()],
                                    choices=[])

    roomWallMaterial = SelectField("Walls Material",
                                    validators=[DataRequired()],
                                    choices=[])

    roomFloorMaterial = SelectField("Floor Material",
                                    validators=[DataRequired()],
                                    choices=[])

    fixtureModel = SelectField("Fixture Model", 
                                    validators=[DataRequired()], 
                                    choices=[])

    floorplanShape = RadioField("Floorplan Shape",
                                validators=[DataRequired()],
                                choices=[])

    luxRequirement = IntegerField("Room Lux Requirement", validators=[DataRequired()])