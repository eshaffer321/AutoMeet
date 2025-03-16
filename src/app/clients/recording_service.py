from pony.orm import db_session, select
from models import Category, Company, Subcategory, Recording
from main.logger import logger

class RecordingClient:

    @classmethod
    @db_session
    def create(cls, filename, category=None, new_category=None, subcategory=None, new_subcategory=None, company=None):
        # Determine the category name: prioritize new_category if provided
        cat_name = new_category or category
        cat_instance = Category.get(name=cat_name)
        if not cat_instance:
            cat_instance = Category(name=cat_name)

        # Determine the subcategory name: prioritize new_subcategory if provided
        subcat_name = new_subcategory or subcategory
        subcat_instance = Subcategory.get(name=subcat_name)
        if not subcat_instance:
            subcat_instance = Subcategory(name=subcat_name, category=cat_instance)

        # Determine the company instance, if company name is provided
        comp_instance = None
        if company:
            comp_instance = Company.get(name=company)
            if not comp_instance:
                comp_instance = Company(name=company)

        # Create the Recording with the entity instances
        Recording(filename=filename,
                category=cat_instance,
                subcategory=subcat_instance,
                company=comp_instance,
                details="Temp details")
