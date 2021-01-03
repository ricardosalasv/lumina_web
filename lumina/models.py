from datetime import datetime
from lumina import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class users(db.Model, UserMixin):
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
    roomArea = db.Column(db.Float)
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