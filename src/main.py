"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Planets, People
#from random import randint
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# read-only: Use this method to generate random members ID's when adding members into the list

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


############# Users #################
@app.route('/user', methods=['GET'])
def get_users():
    users_query = User.query.all()
    result = list(map(lambda x: x.serialize(), users_query)) #Mapea y obtiene lo que necesito //Lista los datos que tiene la tabla serializada
    return jsonify(result), 200 

@app.route('/user', methods=['POST'])
def add_user():
    request_body = json.loads(request.data) #Peticion de los datos, que se cargaran en formato json  // json.loads transcribe a lenguaje de python UTF-8
    if request_body["name"] == None and request_body["email"] == None and request_body["password"] == None and request_body["is_active"] == None:
        return "Datos incompletos, favor completar todos los datos!"
    else:
        user = User(name= request_body["name"], email= request_body["email"], password= request_body["password"], is_active= request_body["is_active"])
        db.session.add(user)
        db.session.commit()
        return "Posteo Exitoso"

@app.route('/user/<int:id>', methods=['DELETE'])
def del_user_by_id(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return("User has been deleted successfully"), 200

############# Favorites #################

############# Planets ###############
@app.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
    result = list(map(lambda x: x.serialize(), planets_query)) #Mapea y obtiene lo que necesito //Lista los datos que tiene la tabla serializada
    return jsonify(result), 200 

@app.route('/planets', methods=['POST'])
def add_planet():
    request_body = json.loads(request.data) #Peticion de los datos, que se cargaran en formato json  // json.loads transcribe a lenguaje de python UTF-8
    if request_body["name"] == None and request_body["climate"] == None and request_body["population"] == None and request_body["orbital"] == None  and request_body["period"] == None and request_body["rotation_period"] == None and request_body["diameter"] == None:
        return "Datos incompletos, favor completar todos los datos!"
    else:
        planet = Planets(name= request_body["name"],climate= str(request_body["climate"]),population= request_body["population"],orbital= request_body["orbital"],period= request_body["period"],rotation_period= request_body["rotation_period"],diameter= request_body["diameter"]) 
        db.session.add(planet)
        db.session.commit()
        return "Posteo Exitoso" 

@app.route('/planets/<int:id>', methods=['DELETE'])
def del_planet_by_id(id):
    planet = Planets.query.filter_by(id=id).first_or_404()
    db.session.delete(planet)
    db.session.commit()
    return("User has been deleted successfully"), 200

############# People ################
#Esta funcion extrae todos los people
@app.route('/people', methods=['GET'])
def get_people():
    people_query = People.query.all()
    result = list(map(lambda x: x.serialize(), people_query)) #Mapea y obtiene lo que necesito //Lista los datos que tiene la tabla serializada
    return jsonify(result), 200 

@app.route('/people', methods=['POST'])
def add_people():
    request_body = json.loads(request.data) #Peticion de los datos, que se cargaran en formato json  // json.loads transcribe a lenguaje de python UTF-8
    if request_body["name"] == None and request_body["birth"] == None and request_body["gender"] == None and request_body["height"] == None  and request_body["skin"] == None and request_body["eye_color"] == None:
        return "Datos incompletos, favor completar todos los datos!"
    else:
        person = People(name= request_body["name"],birth= str(request_body["birth"]),gender= request_body["gender"],height= request_body["height"],skin= request_body["skin"],eye_color= request_body["eye_color"]) 
        db.session.add(person)
        db.session.commit()
        return "Posteo Exitoso" 

@app.route('/people/<int:id>', methods=['DELETE'])
def del_people_by_id(id):
    people = People.query.filter_by(characters_id=id).first_or_404()
    db.session.delete(people)
    db.session.commit()
    return("User has been deleted successfully"), 200


# @app.route('/person/<int:id>', methods=['GET'])
# def get_one_person(id):
#     # fill this method and update the return
#     person = People.query.get(id)
#     return jsonify(person) , 200

# @app.route('/person', methods=['POST'])
# def add_new_person():
#     # fill this method and update the return
#     request_body = json.loads(request.data)
#     personas.add_person(request_body)
#     return jsonify(request_body)

# @app.route('/person/<int:id>', methods=['DELETE'])
# def delete_one_person(id):
#     # fill this method and update the return
#     personas.delete_person(id)
#     return jsonify({"done":True}) , 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
