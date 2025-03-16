from pony.orm import Database, db_session
from models import define_entities

def define_database(**db_params):
    db = Database(**db_params)
    define_entities(db)
    db.generate_mapping(create_tables=True)
    return db

@db_session
def seed_database(db):
    if db.Category.select().count() == 0:  # Only seed if empty
        print("Seeding database...")
        category1 = db.Category(name="Other")
        subcategory1 = db.Subcategory(name="Other", category=category1)
    else:
        print("Database already seeded. Skipping...")