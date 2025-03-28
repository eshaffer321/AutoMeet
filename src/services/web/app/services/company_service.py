from shared.database.models import Company 
from services.web.app.utils.db_utils import get_or_create


class CompanyService:

    @classmethod
    def get_or_create_company(cls, session, company_name):
        """Get or create a category by name."""
        return get_or_create(session, Company, name=company_name)