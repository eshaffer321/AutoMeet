from re import sub
from shared.database.client import SessionLocal
from shared.database.models import Category, Subcategory, Company, Recording
from sqlalchemy.orm import joinedload
from .category_service import CategoryService
from .company_service import CompanyService

class RecordingService:

    @classmethod
    def create(cls, filename, category=None, new_category=None, subcategory=None, new_subcategory=None, company=None):
        """
        Create a recording along with its category, subcategory, and (optional) company.
        Prioritizes new_category and new_subcategory if provided.
        """
        session = SessionLocal()
        try:
            # Determine the category name: prioritize new_category if provided
            cat_name = new_category or category
            cat_instance = CategoryService().get_or_create_category(session, cat_name) 

            # Determine the subcategory name: prioritize new_subcategory if provided
            subcat_name = new_subcategory or subcategory
            subcat_instance = CategoryService().get_or_create_subcategory(session, subcat_name, cat_instance)

            comp_instance = None
            if company:
                comp_instance = CompanyService().get_or_create_company(session, company)
            
            new_recording = Recording(
                s3_key_raw=filename,
                details="Temp details",
                category=cat_instance,
                subcategory=subcat_instance,
                company=comp_instance
            )
            session.add(new_recording)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e  # Optionally log the error as needed
        finally:
            session.close()

    @classmethod
    def update_recording(cls,
        id,
        category=None,
        new_category=None,
        subcategory=None,
        new_subcategory=None,
        company=None,
        speaker_map=None
    ):
        session = SessionLocal()

        cat_name = new_category or category
        category = CategoryService().get_or_create_category(session, cat_name)

        subcat_name = new_subcategory or subcategory
        subcategory = CategoryService().get_or_create_subcategory(session, subcat_name, category)

        if company:
            company = CompanyService().get_or_create_company(session, company)


    @classmethod
    def get_unprocessed(cls):
        """
        Retrieve all recordings with a status of 'unprocessed'.
        """
        session = SessionLocal()
        try:
            unprocessed = session.query(Recording).filter(Recording.status == "unprocessed").all()
            return unprocessed
        finally:
            session.close()

    @classmethod
    def get_recording(cls, id) -> Recording:
        session = SessionLocal()
        try:
            recording = (
                session.query(Recording)
                .options(joinedload(Recording.company))
                .options(joinedload(Recording.category))
                .options(joinedload(Recording.subcategory))
                .filter(Recording.id == id)
                .first()
            )
            return recording
        finally:
            session.close()