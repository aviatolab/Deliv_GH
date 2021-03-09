import csv

from app import app
from app.models import db, Category, Dish

with app.app_context():
    category_entities = []
    with open('delivery_categories.csv') as f:
        reader = csv.reader(f)
        for category_id, title in reader:
            if category_id == 'id':
                continue
            category_entity = Category(title=title)
            db.session.add(category_entity)
            category_entities.append(category_entity)
        db.session.commit()

    with open('delivery_items.csv') as f:
        reader = csv.reader(f)

        for dish_id, title, price, description, picture, category_id in reader:
            if dish_id == 'id':
                continue
            dish_entity = Dish(title=title,
                               price=price,
                               description=description,
                               picture=picture,
                               category=category_entities[int(category_id) - 1])
            db.session.add(dish_entity)
        db.session.commit()
