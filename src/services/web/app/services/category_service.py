from shared.database.models import Category, Subcategory
from services.web.app.utils.db_utils import get_or_create


class CategoryService:

    @classmethod
    def get_or_create_category(cls, session, category_name):
        """Get or create a category by name."""
        return get_or_create(session, Category, name=category_name)

    @classmethod
    def get_or_create_subcategory(cls, session, subcategory_name, category_instance):
        """Get or create a subcategory under a category."""
        return get_or_create(
            session,
            Subcategory,
            name=subcategory_name,
            category_id=category_instance.id if category_instance else None,
        )