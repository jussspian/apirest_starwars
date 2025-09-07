"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import People, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


@app.route('/people', methods=['GET'])
def get_all_people():
    """[GET] /people - Listar todos los registros de people"""
    try:
        people = People.query.all()
        return jsonify([person.serialize() for person in people]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    """[GET] /people/<int:people_id> - Muestra información de un personaje"""
    try:
        person = People.query.get(people_id)
        if not person:
            return jsonify({"error": "People not found"}), 404
        return jsonify(person.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ENDPOINTS DE PLANETS
@app.route('/planets', methods=['GET'])
def get_all_planets():
    """[GET] /planets - Listar todos los registros de planets"""
    try:
        planets = Planet.query.all()
        return jsonify([planet.serialize() for planet in planets]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    """[GET] /planets/<int:planet_id> - Muestra información de un planeta"""
    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404
        return jsonify(planet.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ENDPOINTS DE USERS
@app.route('/users', methods=['GET'])
def get_all_users():
    """[GET] /users - Listar todos los usuarios del blog"""
    try:
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    """[GET] /users/favorites - Listar favoritos del usuario actual"""
    # Por simplicidad, usamos user_id = 1 como usuario actual
    # En una app real, esto vendría del sistema de autenticación
    current_user_id = request.args.get('user_id', 1, type=int)
    
    try:
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        favorites = Favorite.query.filter_by(user_id=current_user_id).all()
        return jsonify([favorite.serialize() for favorite in favorites]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ENDPOINTS PARA AGREGAR FAVORITOS
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    """[POST] /favorite/planet/<int:planet_id> - Añadir planeta favorito"""
    current_user_id = request.json.get('user_id', 1) if request.json else 1
    
    try:
        # Verificar que el planeta existe
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404
            
        # Verificar que el usuario existe
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Verificar que no sea ya un favorito
        existing_favorite = Favorite.query.filter_by(
            user_id=current_user_id, 
            planet_id=planet_id
        ).first()
        
        if existing_favorite:
            return jsonify({"error": "Planet is already in favorites"}), 400
            
        # Crear nuevo favorito
        new_favorite = Favorite(user_id=current_user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({
            "message": "Planet added to favorites successfully",
            "favorite": new_favorite.serialize()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    """[POST] /favorite/people/<int:people_id> - Añadir personaje favorito"""
    current_user_id = request.json.get('user_id', 1) if request.json else 1
    
    try:
        # Verificar que el personaje existe
        person = People.query.get(people_id)
        if not person:
            return jsonify({"error": "People not found"}), 404
            
        # Verificar que el usuario existe
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Verificar que no sea ya un favorito
        existing_favorite = Favorite.query.filter_by(
            user_id=current_user_id, 
            people_id=people_id
        ).first()
        
        if existing_favorite:
            return jsonify({"error": "People is already in favorites"}), 400
            
        # Crear nuevo favorito
        new_favorite = Favorite(user_id=current_user_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({
            "message": "People added to favorites successfully",
            "favorite": new_favorite.serialize()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ENDPOINTS PARA ELIMINAR FAVORITOS
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    """[DELETE] /favorite/planet/<int:planet_id> - Eliminar planeta favorito"""
    current_user_id = request.args.get('user_id', 1, type=int)
    
    try:
        favorite = Favorite.query.filter_by(
            user_id=current_user_id, 
            planet_id=planet_id
        ).first()
        
        if not favorite:
            return jsonify({"error": "Favorite planet not found"}), 404
            
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({"message": "Planet removed from favorites successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    """[DELETE] /favorite/people/<int:people_id> - Eliminar personaje favorito"""
    current_user_id = request.args.get('user_id', 1, type=int)
    
    try:
        favorite = Favorite.query.filter_by(
            user_id=current_user_id, 
            people_id=people_id
        ).first()
        
        if not favorite:
            return jsonify({"error": "Favorite people not found"}), 404
            
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({"message": "People removed from favorites successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)