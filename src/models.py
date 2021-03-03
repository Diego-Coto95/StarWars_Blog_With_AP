from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean

db = SQLAlchemy()
##############################################################################
#Users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(250), unique=False, nullable=False)
    favs = db.relationship("Favorites", lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
#########################################################################
#Favorites
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

#######################################################################
#People
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    birth = db.Column(db.String(250), unique=False, nullable=False)
    gender = db.Column(db.String(250), unique=False, nullable=False)
    height = db.Column(db.Float, unique=False, nullable=False)
    skin = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    hair_color = db.Column(db.String(250), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            # do not serialize the password, its a security breach
        }

#######################################################################
#Planets
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    climate = db.Column(db.String(250), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=True, nullable=False)
    orbital = db.Column(db.Integer, unique=True, nullable=False)
    period = db.Column(db.Integer, unique=True,  nullable=False)
    rotation_period = db.Column(db.Integer, unique=False,  nullable=False)
    diameter = db.Column(db.Integer, unique=True,  nullable=False)
    terrain = db.Column(db.String(250), unique=True,  nullable=False)
    gravity = db.Column(db.Float, unique=True,  nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital,
            "period": self.period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "gravity": self.gravity,

            # do not serialize the password, its a security breach
        }