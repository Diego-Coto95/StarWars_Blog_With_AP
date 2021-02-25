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
from models import db, User, Favorites, Planets, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/users', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    #usuario = User(2, "jfhjf@kf.com")
    #return jsonify(usuario), 200
    return jsonify(User.query.all()), 200


# @app.route('/Users', methods=['GET'])
# def handle_hello():

#     # this is how you can use the Family datastructure by calling its methods
#     members = jackson_family.get_all_members()
#     return jsonify(members), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    # fill this method and update the return
    member = User(id,)
    return jsonify(member) , 200


# @app.route('/member', methods=['POST'])
# def addNewMember():
#     # fill this method and update the return
#     request_body = json.loads(request.data)
#     jackson_family.add_member(request_body)
#     return jsonify(request_body)

# @app.route('/member/<int:id>', methods=['DELETE'])
# def deleteOneMember(id):
#     # fill this method and update the return
#     jackson_family.delete_member(id)
#     return jsonify({"done":True}) , 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
