from re import sub
from venv import logger

from shared.database.client import SessionLocal
from shared.database.models import Category, Subcategory, Company, Recording
from sqlalchemy.orm import joinedload
from .category_service import CategoryService
from .company_service import CompanyService

class RecordingService:

    @classmethod
    def update_recording(cls, id, category_id=None, category_name=None, subcategory_id=None, subcategory_name=None, company=None, speaker_map=None, processed=True):
        session = SessionLocal()
        try:
            recording = cls.get_recording(id, session=session) 
            if not recording:
                raise Exception("Recording not found")
            
            category = CategoryService.resolve_category(session, category_id, category_name)
            recording.category = category

            subcategory = CategoryService.resolve_subcategory(session, subcategory_id, subcategory_name, category)
            recording.subcategory = subcategory

            if company:
                company_obj = CompanyService().get_or_create_company(session, company)
                recording.company = company_obj

            if processed:
                recording.status = "processed"  # type: ignore

            # Optionally handle speaker_map here

            session.commit()
            return recording
        except Exception as e:
            session.rollback()
            raise e
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

    @classmethod
    def get_all_recordings(cls):
        """
        Retrieve all recordings.
        """
        session = SessionLocal()
        try:
            recordings = (
                session.query(Recording)
                .options(joinedload(Recording.company))
                .options(joinedload(Recording.category))
                .options(joinedload(Recording.subcategory))
                .all()
            )
            return recordings
        finally:
            session.close()

    @classmethod
    def get_recording(cls, id, session=None) -> Recording:
        new_session = False
        if not session:
            new_session = True 
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
            if new_session:
                session.close()