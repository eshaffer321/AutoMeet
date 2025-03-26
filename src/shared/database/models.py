from datetime import datetime
from pony.orm import Required, Set, Optional, Database

db = Database() 

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
    id = Required(str, unique=True)
    created_at = Required(datetime, default=datetime.now)
    recording_ended_at = Required(datetime)
    category = Optional(Category)
    subcategory = Optional(Subcategory)
    details = Optional(str)
    company = Optional(Company)  # Nullable - only needed for interviews
