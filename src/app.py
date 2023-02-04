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
from models import db, User, Personajes, Planetas, Vehiculos, Favoritos
#from models import Person

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
    users = User.query.all()
    all_users = list(map(lambda item: item.serialize(),users))

    return jsonify(all_users), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def getUser(user_id):
    users = User.query.filter_by(id=user_id).first()
    if users is None:
        response_body= {
            "msg":"El usuario no existe"
        }
        return jsonify(response_body), 400

    return jsonify(users.serialize()), 200


@app.route('/planetas', methods=['GET'])
def traer_planetas():
    planetas = Planetas.query.all()
    all_planetas = list(map(lambda item: item.serialize(),planetas))

    return jsonify(all_planetas), 200


@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def getPlaneta(planeta_id):
    planetas = Planetas.query.filter_by(id=planeta_id).first()
    if planetas is None:
        response_body= {
            "msg":"El planeta no existe"
        }
        return jsonify(response_body), 400

    return jsonify(planetas.serialize()), 200

@app.route('/personajes', methods=['GET'])
def getPersonaje():
    personajes = Personajes.query.all()
    all_personajes = list(map(lambda item: item.serialize(),personajes))

    return jsonify(all_personajes), 200


@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def getOnepersonaje(personaje_id):
    personajes = Personajes.query.filter_by(id=personaje_id).first()
    if personajes is None:
        response_body= {
            "msg":"El personaje no existe"
        }
        return jsonify(response_body), 400

    return jsonify(personajes.serialize()), 200

@app.route('/vehiculos', methods=['GET'])
def getVehiculo():
    vehiculos = Vehiculos.query.all()
    all_vehiculos = list(map(lambda item: item.serialize(),vehiculos))

    return jsonify(all_vehiculos), 200


@app.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def getOnevehiculo(vehiculo_id):
    vehiculos= Vehiculos.query.filter_by(id=vehiculo_id).first()
    if vehiculos is None:
        response_body= {
            "msg":"El vehiculo no existe"
        }
        return jsonify(response_body), 400

    return jsonify(vehiculos.serialize()), 200


@app.route('/user/<int:user_id>/favoritos', methods=['GET'])
def getFavoritosUser(user_id):
    users = User.query.filter_by(id=user_id).first()
    if users is None:
        response_body= {
            "msg":"El usuario no existe"
        }
        return jsonify(response_body), 400
    favoritos= Favoritos.query.filter_by(user_id=user_id).all()
    all_favoritos = list(map(lambda item: item.serialize(),favoritos))
    return jsonify(all_favoritos), 200

@app.route('/user/<int:user_id>/favoritos/planeta/<int:planeta_id>', methods=['POST'])
def postFavoritosUser(user_id,planeta_id):
    users = User.query.filter_by(id=user_id).first()
    if users is None:
        response_body= {
            "msg":"El usuario no existe"
        }
        return jsonify(response_body), 400

    planeta= Planetas.query.filter_by(id=planeta_id).first()
    if planeta is None:
        response_body= {
            "msg":"El planeta no existe"
        }
        return jsonify(response_body), 400

    favoritos= Favoritos.query.filter_by(planetas_id=planeta_id,user_id=user_id).first()
    if favoritos is not None:
        response_body= {
            "msg":"El planeta ya existe en Favoritos"
        }
        return jsonify(response_body), 400

    newFavoritos=Favoritos(planetas_id=planeta_id,user_id=user_id)
    db.session.add(newFavoritos)
    db.session.commit()
    response_body={
        "msg": "El planeta fue agregado a Favoritos"
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favoritos/personaje/<int:personaje_id>', methods=['POST'])
def postFavoritosPersonajes(user_id,personaje_id):
    users = User.query.filter_by(id=user_id).first()
    if users is None:
        response_body= {
            "msg":"El usuario no existe"
        }
        return jsonify(response_body), 400

    personaje= Personajes.query.filter_by(id=personaje_id).first()
    if personaje is None:
        response_body= {
            "msg":"El personaje no existe"
        }
        return jsonify(response_body), 400

    favoritos= Favoritos.query.filter_by(personajes_id=personaje_id,user_id=user_id).first()
    if favoritos is not None:
        response_body= {
            "msg":"El personaje ya existe en Favoritos"
        }
        return jsonify(response_body), 400

    newFavoritos=Favoritos(personajes_id=personaje_id,user_id=user_id)
    db.session.add(newFavoritos)
    db.session.commit()
    response_body={
        "msg": "El personaje fue agregado a Favoritos"
    }
    return jsonify(response_body), 200


@app.route('/user/<int:user_id>/favoritos/planeta/<int:planeta_id>', methods=['DELETE'])
def deleteFavoritosPlaneta(user_id,planeta_id):
    users = User.query.filter_by(id=user_id).first()
    if users is None:
        response_body= {
            "msg":"El usuario no existe"
        }
        return jsonify(response_body), 400

    planeta= Planetas.query.filter_by(id=planeta_id).first()
    if planeta is None:
        response_body= {
            "msg":"El planeta no existe"
        }
        return jsonify(response_body), 400

    favoritos= Favoritos.query.filter_by(planetas_id=planeta_id,user_id=user_id).first()
    if favoritos is None:
        response_body= {
            "msg":"El planeta no existe en Favoritos"
        }
        return jsonify(response_body), 400

    
    db.session.delete(favoritos)
    db.session.commit()
    response_body={
        "msg": "El planeta fue eliminado de Favoritos"
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favoritos/personaje/<int:personaje_id>', methods=['DELETE'])
def deleteFavoritosPersonaje(user_id,personaje_id):
    users = User.query.filter_by(id=user_id).first()
    if users is None:
        response_body= {
            "msg":"El usuario no existe"
        }
        return jsonify(response_body), 400

    personajes= Personajes.query.filter_by(id=personaje_id).first()
    if personajes is None:
        response_body= {
            "msg":"El personaje no existe"
        }
        return jsonify(response_body), 400

    favoritos= Favoritos.query.filter_by(personajes_id=personaje_id,user_id=user_id).first()
    if favoritos is None:
        response_body= {
            "msg":"El personaje no existe en Favoritos"
        }
        return jsonify(response_body), 400

    
    db.session.delete(favoritos)
    db.session.commit()
    response_body={
        "msg": "El personaje fue eliminado de Favoritos"
    }
    return jsonify(response_body), 200













# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

