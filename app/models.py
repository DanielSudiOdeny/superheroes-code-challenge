from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # Define the relationship from Power to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='power')

    # Define the relationship from Power to Hero through HeroPower
    heroes = db.relationship(
        'Hero', secondary='hero_powers', back_populates='powers')


class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    # Define the relationship from Hero to HeroPower
    hero_powers = db.relationship('HeroPower', back_populates='hero')

    # Define the relationship from Hero to Power through HeroPower
    powers = db.relationship(
        'Power', secondary='hero_powers', back_populates='heroes')


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey(
        'powers.id'), nullable=False)
    strength = db.Column(db.String(255))

    # Define the relationship from HeroPower to Hero
    hero = db.relationship('Hero', back_populates='hero_powers')

    # Define the relationship from HeroPower to Power
    power = db.relationship('Power', back_populates='hero_powers')
