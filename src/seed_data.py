import os
import sys

sys.path.append('src')

from app import app, db
from models import User, People, Planet
from datetime import datetime

def seed_database():
    """Función para poblar la base de datos con datos de prueba"""
    
    with app.app_context():
       
        db.drop_all()
        db.create_all()

        #usuarios de prueba
        user1 = User(
            email="luke@rebels.com",
            password="theforce123",
            first_name="Luke",
            last_name="Skywalker"
        )
        
        user2 = User(
            email="leia@rebels.com", 
            password="princess123",
            first_name="Leia",
            last_name="Organa"
        )
        
        user3 = User(
            email="han@smugglers.com",
            password="falcon123",
            first_name="Han",
            last_name="Solo"
        )
        
        #personajes de prueba
        people1 = People(
            name="Luke Skywalker",
            height="172",
            mass="77",
            hair_color="blond",
            skin_color="fair",
            eye_color="blue",
            birth_year="19BBY",
            gender="male",
            description="A young farm boy from Tatooine who became a Jedi Knight"
        )
        
        people2 = People(
            name="Darth Vader",
            height="202",
            mass="136", 
            hair_color="none",
            skin_color="white",
            eye_color="yellow",
            birth_year="41.9BBY",
            gender="male",
            description="Former Jedi Knight turned Sith Lord"
        )
        
        people3 = People(
            name="Princess Leia",
            height="150",
            mass="49",
            hair_color="brown",
            skin_color="light",
            eye_color="brown", 
            birth_year="19BBY",
            gender="female",
            description="Princess of Alderaan and leader of the Rebel Alliance"
        )
        
        people4 = People(
            name="Obi-Wan Kenobi",
            height="182",
            mass="77",
            hair_color="auburn, white",
            skin_color="fair",
            eye_color="blue-gray",
            birth_year="57BBY", 
            gender="male",
            description="Jedi Master and mentor to Anakin and Luke Skywalker"
        )
        
        people5 = People(
            name="Han Solo",
            height="180",
            mass="80",
            hair_color="brown",
            skin_color="fair",
            eye_color="brown",
            birth_year="29BBY",
            gender="male",
            description="Smuggler captain of the Millennium Falcon"
        )
        
        #planetas de prueba
        planet1 = Planet(
            name="Tatooine",
            climate="arid",
            diameter="10465",
            gravity="1 standard",
            orbital_period="304",
            rotation_period="23",
            population="200000",
            surface_water="1",
            terrain="desert",
            description="A desert world with twin suns in the Outer Rim"
        )
        
        planet2 = Planet(
            name="Alderaan", 
            climate="temperate",
            diameter="12500",
            gravity="1 standard",
            orbital_period="364",
            rotation_period="24",
            population="2000000000",
            surface_water="40",
            terrain="grasslands, mountains",
            description="Peaceful planet destroyed by the Death Star"
        )
        
        planet3 = Planet(
            name="Yavin IV",
            climate="temperate, tropical",
            diameter="10200", 
            gravity="1 standard",
            orbital_period="4818",
            rotation_period="24",
            population="1000",
            surface_water="8",
            terrain="jungle, rainforests",
            description="Forest moon and Rebel Alliance base"
        )
        
        planet4 = Planet(
            name="Hoth",
            climate="frozen",
            diameter="7200",
            gravity="1.1 standard", 
            orbital_period="549",
            rotation_period="23",
            population="unknown",
            surface_water="100",
            terrain="tundra, ice caves, mountain ranges",
            description="Frozen planet used as Rebel base"
        )
        
        planet5 = Planet(
            name="Dagobah",
            climate="murky",
            diameter="8900",
            gravity="N/A",
            orbital_period="341", 
            rotation_period="22",
            population="unknown",
            surface_water="8",
            terrain="swamp, jungles",
            description="Swamp planet where Yoda lived in exile"
        )
        
        
        db.session.add_all([user1, user2, user3])
        db.session.add_all([people1, people2, people3, people4, people5])
        db.session.add_all([planet1, planet2, planet3, planet4, planet5])
        
       
        db.session.commit()
        
        print("Inyectado")

if __name__ == "__main__":
    seed_database()