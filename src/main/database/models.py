from datetime import datetime
from pony.orm import Required, Set, Optional

def define_entities(db):
    class Category(db.Entity):
        name = Required(str, unique=True)
        subcategories = Set("Subcategory")  # One-to-Many relationship
        recordings = Set("Recording")

    class Subcategory(db.Entity):
        name = Required(str)
        category = Required(Category)  # Many-to-One relationship
        recordings = Set("Recording")

    class Company(db.Entity):
        """Only used for interview recordings."""
        name = Required(str, unique=True)
        recordings = Set("Recording")

    class Recording(db.Entity):
        filename = Required(str)
        created_at = Required(datetime, default=datetime.now)
        category = Required(Category)
        subcategory = Required(Subcategory)
        details = Required(str)
        company = Optional(Company)  # Nullable - only needed for interviews
