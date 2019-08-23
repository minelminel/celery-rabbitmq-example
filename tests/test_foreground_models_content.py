import unittest


class TestModelContent(unittest.TestCase):

    def setUp(self):
        from artifice.scraper.foreground.models import db, Content
        self.db = db
        self.Content = Content

    def tearDown(self):
        pass

    def test_model_content_db_is_empty(self):
        result = self.db.session.query(self.Content).all()
        self.assertFalse(result)
        # result <list> empty list return False

    def test_model_content_add_entry(self):
        pass

    def test_model_content_get_entry(self):
        pass

    def test_model_content_add_entry_again(self):
        pass

    def test_model_content_get_entries(self):
        pass
