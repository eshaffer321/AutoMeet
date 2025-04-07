from re import sub
from venv import logger

from shared.database.client import SessionLocal
from shared.database.models import Event 
from sqlalchemy.orm import joinedload

class EventService:

    @classmethod
    def get_all_events(cls):
        """
        Retrieve all events.
        """
        session = SessionLocal()
        try:
            events = (
                session.query(Event)
                .all()
            )
            return events 
        finally:
            session.close()

    @classmethod
    def get_all_events_by_recording_id(cls, recording_id):
        """
        Retrieve all events for a specific recording ID.
        """
        session = SessionLocal()
        try:
            events = (
                session.query(Event)
                .filter(Event.recording_id == recording_id)
                .all()
            )
            return events
        finally:
            session.close()
        