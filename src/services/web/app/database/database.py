from services.web.app.database.models import db
from config.config import settings

def initialize_database():
    """Bind the database to the correct provider only when needed."""
    if not db.provider:  # ✅ Ensures we don’t rebind
        provider = settings.db.provider
        if provider == 'sqlite':
            db.bind(provider='sqlite', filename=':memory:', create_db=True)
        else:
            host = settings.db.host
            port = settings.db.port
            user = settings.db.user
            password = settings.db.password
            database = settings.db.database
            db.bind(user=user, password=password, host=host, database=database, port=port)

        db.generate_mapping(create_tables=True)

def get_database():
    """Ensure `db` is initialized before returning it."""
    if not db.provider:
        raise RuntimeError("Database is not initialized! Call `initialize_database()` first.")
    return db

