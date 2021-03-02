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
from models import db, User, Favorites, People, Planets
import datetime

## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# read-only: Use this method to generate random members ID's when adding members into the list

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#################################################### Users #########################################################
@app.route('/user', methods=['GET'])
def get_users():
    users_query = User.query.all() #Query es una consulta
    result = list(map(lambda x: x.serialize(), users_query)) #Mapea y obtiene lo que necesito //Lista los datos que tiene la tabla serializada
    return jsonify(result), 200 

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first_or_404()
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['POST'])
def add_user():
    request_body = json.loads(request.data) #Peticion de los datos, que se cargaran en formato json  // json.loads transcribe a lenguaje de python UTF-8
    if request_body["name"] == None and request_body["email"] == None:
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

#################################################### Favorites ########################################################

@app.route('/favorites', methods=['GET'])
def get_favorites():
    fav_query = Favorites.query.all()
    result = list(map(lambda x: x.serialize(), fav_query)) #Mapea y obtiene lo que necesito //Lista los datos que tiene la tabla serializada
    return jsonify(result), 200 

@app.route('/favorites', methods=['POST'])
def add_fav():
    # recibir info del request
    request_body = request.get_json()
    print(request_body)
    fav = Favorites(name=request_body["name"], uid=request_body['uid'])
    db.session.add(fav)
    db.session.commit()
    return jsonify("All good"), 200


@app.route('/favorites/<int:fid>', methods=['PUT'])
def update_fav(fid):
    # recibir info del request
    fav = Favorites.query.get(fid)
    if fav is None:
        raise APIException('Favorite not found', status_code=404)
    request_body = request.get_json()
    if "name" in request_body:
        fav.name = request_body["name"]
    db.session.commit()
    return jsonify("All good"), 200


@app.route('/favorites/<int:fid>', methods=['DELETE'])
def del_fav(fid):
    # recibir info del request
    fav = Favorites.query.get(fid)
    if fav is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(fav)
    db.session.commit()
    return jsonify("All good"), 200



#################################################### People ###########################################################
#Esta funcion extrae todos los people
@app.route('/people', methods=['GET'])
def get_people():
    people_query = People.query.all()
    result = list(map(lambda x: x.serialize(), people_query)) #Mapea y obtiene lo que necesito //Lista los datos que tiene la tabla serializada
    return jsonify(result), 200 

@app.route('/people/<int:id>', methods=['GET'])
def get_people_by_id(id):
    people = People.query.filter_by(id=id).first_or_404()
    return jsonify(people.serialize()), 200

@app.route('/people', methods=['POST'])
def add_people():
    request_body = json.loads(request.data) #Peticion de los datos, que se cargaran en formato json  // json.loads transcribe a lenguaje de python UTF-8
    if request_body["name"] == None and request_body["birth"] == None and request_body["gender"] == None and request_body["height"] == None  and request_body["skin"] == None and request_body["eye_color"] == None and request_body["hair_color"] == None:
        return "Datos incompletos, favor completar todos los datos!"
    else:
        person = People(name= request_body["name"],birth= str(request_body["birth"]),gender= request_body["gender"],height= request_body["height"],skin= request_body["skin"],eye_color= request_body["eye_color"],hair_color= request_body["hair_color"]) 
        db.session.add(person)
        db.session.commit()
        return "Posteo Exitoso" 

@app.route('/people/<int:id>', methods=['DELETE'])
def del_people_by_id(id):
    people = People.query.filter_by(id=id).first_or_404()
    db.session.delete(people)
    db.session.commit()
    return("User has been deleted successfully"), 200


#################################################### Planets ###################################################################

@app.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
    result = list(map(lambda x: x.serialize(), planets_query)) #Mapea y obtiene lo que necesito //Lista los datos que tiene la tabla serializada
    return jsonify(result), 200 

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planets.query.filter_by(id=id).first_or_404()
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def add_planet():
    request_body = json.loads(request.data) #Peticion de los datos, que se cargaran en formato json  // json.loads transcribe a lenguaje de python UTF-8
    if request_body["name"] == None and request_body["climate"] == None and request_body["population"] == None and request_body["orbital"] == None  and request_body["period"] == None and request_body["rotation_period"] == None and request_body["diameter"] == None and request_body["terrain"] == None and request_body["gravity"] == None:
        return "Datos incompletos, favor completar todos los datos!"
    else:
        planet = Planets(name= request_body["name"],climate= str(request_body["climate"]),population= request_body["population"],orbital= request_body["orbital"],period= request_body["period"],rotation_period= request_body["rotation_period"],diameter= request_body["diameter"],terrain= request_body["terrain"],gravity= request_body["gravity"]) 
        db.session.add(planet)
        db.session.commit()
        return "Posteo Exitoso" 

@app.route('/planets/<int:id>', methods=['DELETE'])
def del_planet_by_id(id):
    planet = Planets.query.filter_by(id=id).first_or_404()
    db.session.delete(planet)
    db.session.commit()
    return("User has been deleted successfully"), 200


################################################### REGISTER ##########################################################
@app.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "email is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"msg": "Username  already exists"}), 400

        user = User()
        user.email = email
        hashed_password = generate_password_hash(password)
        print(password, hashed_password)
        user.password = hashed_password
        db.session.add(user)
        db.session.commit()

        return jsonify({"success": "Thanks. your register was successfully", "status": "true"}), 200

############################################## LOGIN ######################################################

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "Username is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        # crear el token
        expiracion = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.email, expires_delta=expiracion)

        data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000
        }

        return jsonify(data), 200

################################### PROFILE ####################################################

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    if request.method == 'GET':
        token = get_jwt_identity()
        return jsonify({"success": "Acceso a espacio privado", "usuario": token}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
