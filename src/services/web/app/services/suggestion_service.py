from sqlalchemy.orm import Session
from sqlalchemy import func
from shared.database.client import SessionLocal
from shared.database.models import Category, Company, Subcategory, Recording

class SuggestionsService:
    # Assuming these are defined somewhere in your class
    _recording_types = []
    _companies = []
    _meeting_types = []

    @classmethod
    def get_categories(cls):
        """
        Return the categories ranked by most frequently used.
        """
        with SessionLocal() as session:
            # Outer join to include categories with no recordings
            results = (
                session.query(
                    Category.id,
                    Category.name,
                    func.count(Recording.id).label("recording_count")
                )
                .outerjoin(Recording, Category.id == Recording.category_id)
                .group_by(Category.id)
                .order_by(func.count(Recording.id).desc())
                .all()
            )
            # Build list of dicts from the query results
            categories = [
                {"id": row.id, "name": row.name, "recording_count": row.recording_count or 0}
                for row in results
            ]
        return categories

    @classmethod
    def get_companies(cls):
        """
        Return all companies.
        """
        with SessionLocal() as session:
            companies = session.query(Company).all()
            return [{"id": c.id, "name": c.name} for c in companies]

    @classmethod
    def get_sub_categories(cls, category_name):
        """
        Return the subcategories for a given category, ranked by most frequently used.
        """
        with SessionLocal() as session:
            # Find the category by name
            category = session.query(Category).filter(Category.name == category_name).first()
            if not category:
                return []
            
            results = (
                session.query(
                    Subcategory.id,
                    Subcategory.name,
                    func.count(Recording.id).label("recording_count")
                )
                .outerjoin(Recording, Subcategory.id == Recording.subcategory_id)
                .filter(Subcategory.category_id == category.id)
                .group_by(Subcategory.id)
                .order_by(func.count(Recording.id).desc())
                .all()
            )
            subcategories = [
                {"id": row.id, "name": row.name, "recording_count": row.recording_count or 0}
                for row in results
            ]
        return subcategories

    @classmethod
    def add_suggestion(cls, category, value):
        """
        Dynamically add new values to a suggestion category.
        This method simply updates in-memory lists.
        """
        if category == "recording-type" and value not in cls._recording_types:
            cls._recording_types.append(value)
        elif category == "company" and value not in cls._companies:
            cls._companies.append(value)
        elif category == "meeting-type" and value not in cls._meeting_types:
            cls._meeting_types.append(value)