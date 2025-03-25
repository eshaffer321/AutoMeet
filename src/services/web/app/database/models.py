from datetime import datetime
from pony.orm import Required, Set, Optional, Database

db = Database() 

def define_entities():
    """Define database entities and attach them to `db`."""
    global Category, Subcategory, Company, Recording 

    class Category(db.Entity):
        name = Required(str, unique=True)
        subcategories = Set("Subcategory")
        recordings = Set("Recording")

    class Subcategory(db.Entity):
        name = Required(str)
        category = Required(Category)
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

define_entities()  