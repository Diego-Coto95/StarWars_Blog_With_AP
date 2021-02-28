from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, Date
from random import randint

db = SQLAlchemy()
##############################################################################
#Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

#########################################################################
#Favorites
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    Type = db.Column(db.Boolean, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.email,
            "Type": self.Type,
            # do not serialize the password, its a security breach
        }

#######################################################################
#Planets
class Planets(db.Model):
    planets_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    climate = db.Column(db.String(250), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=True, nullable=False)
    orbital = db.Column(db.Integer, unique=True, nullable=False)
    period = db.Column(db.Integer, unique=True,  nullable=False)
    rotation_period = db.Column(db.Integer, unique=False,  nullable=False)
    diameter = db.Column(db.Integer, unique=True,  nullable=False)

    def serialize(self):
        return {
            "planets_id": self.planets_id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "orbital": self.orbital,
            "period": self.period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
            # do not serialize the password, its a security breach
        }

#######################################################################
#People
class People(db.Model):
    characters_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    birth = db.Column(db.String, unique=False, nullable=False)
    gender = db.Column(db.String(250), unique=False, nullable=False)
    height = db.Column(db.Float, unique=False, nullable=False)
    skin = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)

    def serialize(self):
        return {
            "characters_id": self.characters_id,
            "name": self.name,
            "birth": self.birth,
            "gender": self.gender,
            "height": self.height,
            "skin": self.skin,
            "eye_color": self.eye_color,
            # do not serialize the password, its a security breach
        }