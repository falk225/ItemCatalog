from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = ['Baseball', 'Boxing', 'Camping', 'Painting', 'Road Tripping']
for category in categories:
    session.add(Category(name=category))
session.commit()

items = [['Bat', 'A long object used for hitting the ball. Often wooden or made of metal.', 1],
        ['Glove', 'A large leather glove or mit that helps the player catch the ball.', 1],
        ['Cleats', 'Special shoes with hard toes and spiked bottoms to protect the player and increase their traction.', 1],
        ['Gloves', 'Padded gloves that protect your hands and your opponent.', 2],
        ['Wrist Wraps', 'Thin strips of cloth that support your wrist.', 2],
        ['Tent', 'A simple cloth building that provides basic protection against the elements.', 3],
        ['Sleeping Bag', 'An insulated cloth bag that keeps the user warm at night when they are sleeping.', 3],
        ['Matches', 'Small sticks that when struck burst into flame allowing the user to start a fire.', 3],
        ['Paint Brushes', 'Small sticks with hairy tips for applying paint.', 4],
        ['Paints', 'Colored pigments for creating pictures on parchment.', 4],
        ['Car', 'An Automobile that consumes gas and travels quickly along roads.', 5],
        ['CDs', 'Small circles that hold music for jammin while driving.', 5],
        ['Snacks', 'Delicious food items, necessary for maintaining morale when the trip is taking a long time.', 5],
        ['Coffee', 'A special drink that keeps the drinker awake so they can continue driving longer.', 5]
        ]

for item in items:
    session.add(Item(name=item[0], description=item[1], category_id=item[2]))
session.commit()

print('Records Added!')
