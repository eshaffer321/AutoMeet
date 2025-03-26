from shared.database.database import get_database
from pony.orm import db_session
from shared.util.logging import logger

@db_session
def seed_database():
    """Seed initial production data into the database, only if empty."""
    db = get_database()

    # Check if we already have data
    if db.Category.select().count() > 0:
        logger.info("✅ Database already seeded. Skipping...")
        return

    logger.info("🌱 Seeding database with initial data...")

    # Seed categories
    category1 = db.Category(name="Other")
    db.Subcategory(name="Other", category=category1)

    logger.info("✅ Seeding complete!")