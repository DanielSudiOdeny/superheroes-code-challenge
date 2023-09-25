#!/usr/bin/env python3

from models import db, Hero, Power
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''


@app.route('/heroes', methods=['GET'])
def heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
            "name": hero.name,
            "super_name": hero.super_name,
            "created_at": hero.created_at,
            "updated_at": hero.updated_at,
            "powers": [
                {'id': power.id,
                 'name': power.name,
                 'description': power.description
                 }
                for power in hero.powers
            ]
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


if __name__ == '__main__':
    app.run(port=5555)
