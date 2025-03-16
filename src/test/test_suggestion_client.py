import unittest
from pony.orm import db_session, select, count, Database
from models import Category, Company, Recording, Subcategory, db, setup_database
from clients.suggestion_client import SuggestionsClient


class TestCategoryRecordings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test database once for all tests."""
        setup_database(testing=True)  # Use in-memory DB for tests
        cls.suggestion_client = SuggestionsClient()


    def setUp(self):
        """Set up test data before each test."""
        db.drop_all_tables(with_all_data=True)  # No @db_session needed
        db.create_tables()

        with db_session:  # Now we open a session for adding data
            # Create Categories
            self.cat1 = Category(name="Interviews")
            self.cat2 = Category(name="Meetings")
            self.cat3 = Category(name="Other")

            # Create Subcategories
            self.sub1 = Subcategory(name="Tech", category=self.cat1)
            self.sub2 = Subcategory(name="General", category=self.cat2)
            self.sub3 = Subcategory(name="Misc", category=self.cat3)

            # Create Recordings
            Recording(filename="interview1.mp3", category=self.cat1, subcategory=self.sub1, details="Tech Interview")
            Recording(filename="interview2.mp3", category=self.cat1, subcategory=self.sub1, details="Tech Interview")
            Recording(filename="meeting1.mp3", category=self.cat2, subcategory=self.sub2, details="Team Meeting")
            Recording(filename="meeting2.mp3", category=self.cat2, subcategory=self.sub2, details="Scrum Call")
            Recording(filename="meeting3.mp3", category=self.cat2, subcategory=self.sub2, details="1-on-1")


    @db_session
    def test_recording_counts(self):
        """Test that the recording counts are correct."""
        self.assertEqual(self.cat1.recordings.count(), 2)  # Interviews has 2 recordings
        self.assertEqual(self.cat2.recordings.count(), 3)  # Meetings has 3 recordings
        self.assertEqual(self.cat3.recordings.count(), 0)  # Other has 0 recordings

    @db_session
    def test_sorted_categories(self):
        """Test that categories are sorted by recording count."""
        categories = self.suggestion_client.get_categories()
        sorted_names = [c['name'] for c in categories]
        self.assertEqual(sorted_names, ["Meetings", "Interviews", "Other"])  # Meetings (3), Interviews (2), Other (0)

    @db_session
    def test_sorted_subcategories(self):
        """Test that subcategories are sorted correctly within a category."""
        subcategories = self.suggestion_client.get_sub_categories("Interviews")
        sorted_names = [s['name'] for s in subcategories]
        self.assertEqual(sorted_names, ["Tech"])  # Tech has 2 recordings, should be first

        subcategories = self.suggestion_client.get_sub_categories("Meetings")
        sorted_names = [s['name'] for s in subcategories]
        self.assertEqual(sorted_names, ["General"])  # General has 3 recordings, should be first

    @db_session
    def test_get_subcategories_invalid_category(self):
        """Test that getting subcategories for a non-existent category returns an empty list."""
        subcategories = self.suggestion_client.get_sub_categories("NonExistent")
        self.assertEqual(subcategories, [])  # Should return an empty list for invalid categories


if __name__ == '__main__':
    unittest.main()