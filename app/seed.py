from random import choice
from app import app, db
from models import Power, Hero, HeroPower

with app.app_context():
    print("🦸‍♀ Seeding powers...")
    powers_data = [
        {"name": "super strength",
            "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses",
            "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    for data in powers_data:
        power = Power(**data)
        db.session.add(power)

    db.session.commit()

    print("🦸‍♀ Seeding heroes...")
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for data in heroes_data:
        hero = Hero(**data)
        db.session.add(hero)

    db.session.commit()

    print("🦸‍♀ Adding powers to heroes...")

    strengths = ["Strong", "Weak", "Average"]

    for hero in Hero.query.all():
        for _ in range(1, 4):  
            power = choice(Power.query.all())
            strength = choice(strengths)

            hero_power = HeroPower(hero=hero, power=power, strength=strength)
            db.session.add(hero_power)

    db.session.commit()

    print("🦸‍♀ Done seeding!")
