#!/usr/bin/env python3

from flask import request, jsonify, make_response
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


# @app.route('/')
# def home():
#     return ''


@app.route('/heroes', methods=["GET"])
def heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        heroes.append(hero_dict)

    response = make_response(jsonify(heroes), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/heroes/<int:id>', methods=['GET'])
def hero_by_id(id):
    hero = Hero.query.filter_by(id=id).first()

    if not hero:
        return jsonify({'error': "Hero not found", }, 404)

    hero_dict = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [
            {'id': power.id,
             'name': power.name,
             'description': power.description
             }
            for power in hero.powers
        ]
    }
    response = make_response(jsonify(hero_dict), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/powers', methods=['GET'])
def powers():
    powers = []

    for power in Power.query.all():
        power_dict = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        powers.append(power_dict)

    response = make_response(jsonify(powers), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    power_dict = {
        'id': power.id,
        'name': power.name,
        'description': power.description,
    }
    response = make_response(jsonify(power_dict), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/powers/<int:id>', methods=['PATCH'])
def patch_power_by_id(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    for attr in request.json:
        setattr(power, attr, request.json.get(attr))

        db.session.add(power)
        db.session.commit()

    power_dict = {
        'id': power.id,
        'name': power.name,
        'description': power.description,

    }
    response = make_response(jsonify(power_dict), 200)
    return response


# ... (other imports)


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    # Validate the required fields
    if "strength" not in data or "power_id" not in data or "hero_id" not in data:
        return jsonify({"errors": ["strength, power_id, and hero_id fields are required"]}), 400

    strength = data["strength"]
    power_id = data["power_id"]
    hero_id = data["hero_id"]

    # Check if the Power and Hero exist
    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)

    if power is None or hero is None:
        return jsonify({"errors": ["Power or Hero not found"]}), 404

    # Create a new HeroPower
    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    try:
        db.session.add(hero_power)
        db.session.commit()
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        response = make_response(
            jsonify(hero_data),
            200
        )
        return response  # Correct indentation for returning the response
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400


app.route('/')

if __name__ == '__main__':
    app.run(port=5555)
