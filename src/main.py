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
from models import db, User, Planet, Character, Favorite
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

@app.route('/testuser', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/users", methods=["GET"])
def get_User():
    users=User.query.all()
    request=list(map(lambda user:user.serialize(), users))
    return jsonify(request), 200

@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_FavoritebyUserID(user_id):
    favorites=Favorite.query.filter_by(idUser=user_id)
    if favorites is None:
        raise APIException("Msg: user not found", status_code=404)
    request=list(map(lambda favorite:favorite.serialize(), favorites))
    return jsonify(request), 200

#@app.route("/users/<int:user_id>/favorites", methods=["POST"])
#def create_favorite():
 #   data = request.get_json()
  #  favorite1= Favorite(username=data["username"], planet=data["email"], character=data["character"])
   # db.session.add(favorite1)
    #db.session.commit()
    #return jsonify("Message: user added"), 200

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    user1= User(username=data["username"], email=data["email"], password=data["password"])
    db.session.add(user1)
    db.session.commit()
    return jsonify("Message: user added"), 200


@app.route("/planets", methods=["GET"])
def get_Planet():
    planets=Planet.query.all()
    response=list(map(lambda planet:planet.serialize(), planets))
    return jsonify(response), 200


@app.route("/planets/<int:id>" , methods=["GET"] )  
def get_PlanetId(id):
    planet=Planet.query.filter_by(id=id).first()
    if planet is None:
        raise APIException("Msg: planet not found", status_code=404)
    request= planet.serialize()
    return jsonify(request), 200

@app.route("/people", methods=["GET"])
def get_Character():
    characters=Character.query.all()
    response=list(map(lambda character:character.serialize(), characters))
    return jsonify(response), 200

@app.route("/people/<int:id>" , methods=["GET"] )  
def get_CharacterId(id):
    character=Character.query.filter_by(id=id).first()
    if character is None:
        raise APIException("Msg: character not found", status_code=404)
    request= character.serialize()
    return jsonify(request), 200    

@app.route("/favorite/<int:favorite_id>", methods=["DELETE"])
def delete_favorite():
    favorite = Favorite.query.get(idUser)
    if favorite is None:
     raise APIException('User not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()    
    return jsonify("Message: user added"), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
