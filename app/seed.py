from random import randint, choice
from app import app, db
from models import Hero, Power, HeroPower

# List of superhero names
superhero_names = ['Superman', 'Batman', 'Spiderman', 'Ironman', 'Thor',
                   'Hulk', 'Captain America', 'Black Widow', 'Hawkeye', 'Starlord']

# List of real names corresponding to the superhero names
real_names = ['Clark Kent', 'Bruce Wayne', 'Peter Parker', 'Tony Stark', 'Thor Odinson',
              'Bruce Banner', 'Steve Rogers', 'Natasha Romanoff', 'Clint Barton', 'Peter Quill']

# List of powers
powers_list = ['Super Strength', 'Flight', 'Invulnerability',
               'Super Speed', 'Heat Vision', 'Freeze Breath']

with app.app_context():
    db.drop_all()
    db.create_all()

    heroes = []
    for _ in range(20):
        hero = Hero(
            name=choice(real_names),
            super_name=choice(superhero_names),
        )
        heroes.append(hero)
        db.session.add(hero)

    powers = []
    for _ in range(20):
        power = Power(
            name=choice(powers_list),
            description=f'This power allows the hero to use {choice(powers_list).lower()}'
        )
        powers.append(power)
        db.session.add(power)

    db.session.commit()

    strengths = ["Strong", "Weak", "Average"]

    for hero in heroes:
        for _ in range(1, 4):  # Randomly add up to 3 powers to each hero
            power = choice(powers)
            strength = choice(strengths)
            hero_power = HeroPower(
                hero=hero,
                power=power,
                strength=strength
            )
            db.session.add(hero_power)

    db.session.commit()

print("Seeding completed successfully.")
