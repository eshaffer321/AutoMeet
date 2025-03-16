from app.database.models import db


def initialize_database(**db_params):
    """Bind the database to the correct provider only when needed."""
    if not db.provider:  # ✅ Ensures we don’t rebind
        db.bind(**db_params)
        db.generate_mapping(create_tables=True)

def get_database():
    """Ensure `db` is initialized before returning it."""
    if not db.provider:
        raise RuntimeError("Database is not initialized! Call `initialize_database()` first.")
    return db

