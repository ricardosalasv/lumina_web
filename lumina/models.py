from datetime import datetime
from lumina import db, login_manager
from sqlalchemy import Table, Column
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Foreign keys
    projects = db.relationship('Projects', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, '{self.email}')"

class Projects(db.Model): # Created projects

    id = db.Column(db.Integer, primary_key=True)

    # Physical space aspects
    projectCode = db.Column(db.String(40))
    name = db.Column(db.String(40))
    roomLength = db.Column(db.Float, default=0)
    roomWidth = db.Column(db.Float, default=0)
    roomHeight = db.Column(db.Float, default=0)
    roomArea = db.Column(db.Float, default=0)
    roomCeilingMaterial = db.Column(db.String(40))
    roomWallMaterial = db.Column(db.String(40))
    roomFloorMaterial = db.Column(db.String(40))
    luxRequirement = db.Column(db.Integer, default=0)
    amountOfFixtures = db.Column(db.Integer, default=0)
    totalProjectCost = db.Column(db.Float, default=0)
    dateModified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)
    fpShape_id = db.Column(db.Integer, db.ForeignKey('floorplan_shapes.id'), nullable=False)

    @property
    def serialized(self):

        return {
            "id" : self.id,
            "name": self.name,
            "roomLength" : self.roomLength,
            "roomWidth" : self.roomWidth,
            "roomHeight" : self.roomHeight,
            "roomArea" : self.roomArea,
            "roomCeilingMaterial" : self.roomCeilingMaterial,
            "roomWallMaterial" : self.roomWallMaterial,
            "roomFloorMaterial" : self.roomFloorMaterial,
            "luxRequirement" : self.luxRequirement,
            "amountOfFixtures" : self.amountOfFixtures,
            "totalProjectCost" : self.totalProjectCost,
            "user_id" : self.user_id,
            "model_id" : self.model_id,
            "fpShape_id" : self.fpShape_id,
        }

    def __repr__(self):
        return f"Project({self.id}, '{self.name}', '{self.projectCode}', {self.user_id}, {self.model_id}, {self.fpShape_id})"

class Floorplan_Shapes(db.Model): # Rectangular or irregular

    __tablename__ = "floorplan_shapes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f"Floorplan_Shape('{self.name}')"

class Brands(db.Model): # Available brands

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    # Foreign keys
    models = db.relationship('Models', backref='brand', lazy=True)

    def __repr__(self):
        return f"Brand('{self.id}, {self.name}')"

class Models(db.Model): # Available fixture models
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    mark = db.Column(db.String(20), unique=True)
    productCode = db.Column(db.String(20))
    lm = db.Column(db.Integer, default=0)
    w = db.Column(db.Integer, default=0)
    fixtureType = db.Column(db.String(20), default="Rectangular")
    length = db.Column(db.Float, default=0)
    width = db.Column(db.Float, default=0)
    height = db.Column(db.Float, default=0)
    diameter = db.Column(db.Float, default=0)
    temperature = db.Column(db.Integer, default=4000)
    usage = db.Column(db.String(40), default='General')
    price = db.Column(db.Float, default=0)

    # Foreign keys
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    finish_id = db.Column(db.Integer, db.ForeignKey('finishes.id'), nullable=False)

    def __repr__(self):
        return f"""Model('{self.name}, '{self.mark}', '{self.productCode}', '{self.lm}', '{self.w}', '{self.temperature}', '{self.usage}', '{self.price}')"""

    @property
    def serializedForProject(self):

        return {
            "id" : self.id,
            "name": self.name,
            "price": self.price,
            "lm": self.lm,
            "brand" : self.brand.name,
            "finish" : self.finish.name,
        }

class Finishes(db.Model): # Available finishes for the fixtures

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    # Foreign keys
    models = db.relationship('Models', backref='finish', lazy=True)
    type_id = db.Column(db.Integer, db.ForeignKey('material_types.id'), nullable=False)

    def __repr__(self):
        return f"Finish('{self.id}, {self.name}')"

class Arch_Materials(db.Model): # Available finishes for the fixtures

    __tablename__ = "arch_materials"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    albedo = db.Column(db.Float, default=0.7)

    # Foreign keys
    type_id = db.Column(db.Integer, db.ForeignKey('material_types.id'), nullable=False)

    def __repr__(self):
        return f"ArchMaterial('{self.name}')"

class Material_Types(db.Model): # Contains the type of materials or finishes; plastic, metal, paint, etc

    __tablename__ = "material_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    def __repr__(self):
        return f"Material_Type('{self.name}')"

projects_materials = Table('projects_materials', db.Model.metadata,
    Column('project_id', db.ForeignKey('projects.id')),
    Column('archmaterial_id', db.ForeignKey('arch_materials.id'))
)