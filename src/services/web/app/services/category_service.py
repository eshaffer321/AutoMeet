from shared.database.models import Category, Subcategory
from services.web.app.utils.db_utils import get_or_create


class CategoryService:

    @classmethod
    def get_or_create_category(cls, session, category_name):
        # This will look for a Category with the given name; if it doesn't exist, it creates one.
        return get_or_create(session, Category, name=category_name)

    @classmethod
    def get_or_create_subcategory(cls, session, subcategory_name, category_instance):
        # Ensure that the subcategory is tied to the provided category.
        return get_or_create(session, Subcategory, name=subcategory_name, category_id=category_instance.id)

    @classmethod
    def resolve_category(cls, session, category_id, category_name):
        if category_id:
            category = session.query(Category).get(category_id)
            if not category:
                raise Exception("Category with given id does not exist.")
            return category
        elif category_name:
            return cls.get_or_create_category(session, category_name)
        return None

    @classmethod
    def resolve_subcategory(cls, session, subcategory_id, subcategory_name, category_instance):
        if subcategory_id:
            subcategory = session.query(Subcategory).get(subcategory_id)
            if not subcategory:
                raise Exception("Subcategory with given id does not exist.")
            return subcategory
        elif subcategory_name:
            return cls.get_or_create_subcategory(session, subcategory_name, category_instance)
        return None