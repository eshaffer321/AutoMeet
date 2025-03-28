from shared.database.client import SessionLocal
from shared.database.models import Category, Subcategory
from shared.util.logging import logger

def seed_database():
    """Seed initial production data into the database, only if empty."""
    session = SessionLocal()
    try:
        # Check if we already have data by counting existing categories
        if session.query(Category).count() > 0:
            logger.info("✅ Database already seeded. Skipping...")
            return

        logger.info("🌱 Seeding database with initial data...")

        # Create the "Other" category
        category1 = Category(name="Other")
        session.add(category1)
        session.commit()  # Commit so that category1 gets an ID

        # Create a "Other" subcategory tied to the category above
        subcategory_other = Subcategory(name="Other", category=category1)
        session.add(subcategory_other)
        session.commit()

        logger.info("✅ Seeding complete!")
    except Exception as e:
        session.rollback()
        logger.error("❌ Error seeding database", exc_info=True)
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()