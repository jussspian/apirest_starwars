from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///starwars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelos de la base de datos (usando los del proyecto anterior)
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    subscription_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None
        }

class People(db.Model):
    __tablename__ = 'people'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(20))
    mass = db.Column(db.String(20))
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    description = db.Column(db.Text)
    
    favorites = db.relationship("Favorite", back_populates="people")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "description": self.description
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100))
    diameter = db.Column(db.String(50))
    gravity = db.Column(db.String(50))
    orbital_period = db.Column(db.String(50))
    rotation_period = db.Column(db.String(50))
    population = db.Column(db.String(50))
    surface_water = db.Column(db.String(50))
    terrain = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    favorites = db.relationship("Favorite", back_populates="planet")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "population": self.population,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
            "description": self.description
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", back_populates="favorites")
    people = db.relationship("People", back_populates="favorites")
    planet = db.relationship("Planet", back_populates="favorites")
    
    def serialize(self):
        favorite_item = {}
        if self.people_id:
            favorite_item = {
                "type": "people",
                "id": self.people_id,
                "name": self.people.name if self.people else None
            }
        elif self.planet_id:
            favorite_item = {
                "type": "planet", 
                "id": self.planet_id,
                "name": self.planet.name if self.planet else None
            }
            
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_item": favorite_item,
            "date_added": self.date_added.isoformat() if self.date_added else None
        }
