from pony.orm import db_session, select, count
from models import Category, Company, Subcategory
class SuggestionsClient:

    @classmethod
    @db_session
    def get_categories(cls):
        """ Return the categories ranked by most frequenly used """
        categories = [
            {"id": c.id, "name": c.name, "recording_count": rec_count or 0}
            for c, rec_count in select(
                (c, count(c.recordings)) for c in Category
            )
        ]
        return [c for c in sorted(categories, key=lambda x: -x["recording_count"])]

    @classmethod
    @db_session
    def get_companies(cls):
        return [{"id": c.id, "name": c.name} for c in Company.select()] 

    @classmethod
    @db_session
    def get_sub_categories(cls, category_name):
        """ Return the subcategories ranked by most frequently used """
        category = Category.get(name=category_name)  # Find the category
        if not category:
            return []  # Return empty if category not found
        
        subcategories = [
            {"id": s.id, "name": s.name, "recording_count": rec_count or 0}
            for s, rec_count in select(
                (s, count(s.recordings)) for s in Subcategory if s.category == category
            )
        ]
        return sorted(subcategories, key=lambda x: -x["recording_count"])

    @classmethod
    @db_session
    def add_suggestion(cls, category, value):
        """Dynamically add new values to a category"""
        if category == "recording-type" and value not in cls._recording_types:
            cls._recording_types.append(value)
        elif category == "company" and value not in cls._companies:
            cls._companies.append(value)
        elif category == "meeting-type" and value not in cls._meeting_types:
            cls._meeting_types.append(value)