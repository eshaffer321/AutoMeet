from shared.database.client import SessionLocal
from shared.database.models import Category, Subcategory, Company, Recording

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
            cat_instance = session.query(Category).filter(Category.name == cat_name).first()
            if not cat_instance:
                cat_instance = Category(name=cat_name)
                session.add(cat_instance)
                session.commit()  # Commit so that the category gets an ID
                session.refresh(cat_instance)

            # Determine the subcategory name: prioritize new_subcategory if provided
            subcat_name = new_subcategory or subcategory
            subcat_instance = session.query(Subcategory).filter(Subcategory.name == subcat_name).first()
            if not subcat_instance:
                subcat_instance = Subcategory(name=subcat_name, category=cat_instance)
                session.add(subcat_instance)
                session.commit()  # Commit to assign an ID and persist the relation
                session.refresh(subcat_instance)

            # Determine the company instance, if a company name is provided
            comp_instance = None
            if company:
                comp_instance = session.query(Company).filter(Company.name == company).first()
                if not comp_instance:
                    comp_instance = Company(name=company)
                    session.add(comp_instance)
                    session.commit()  # Commit to persist the new company
                    session.refresh(comp_instance)

            # Create the Recording record.
            # Here, we're mapping the passed filename to the s3_key_raw field.
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