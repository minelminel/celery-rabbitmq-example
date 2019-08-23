import unittest


class TestModelQueue(unittest.TestCase):

    def setUp(self):
        from artifice.scraper.foreground.models import db, Queue
        self.db = db
        self.Queue = Queue

    def tearDown(self):
        pass

    def test_model_db_is_empty(self):
        result = self.db.session.query(self.Queue).all()
        self.assertFalse(result)
        # result <list> empty list return False

    def test_model_query_add_entry(self):
        pass

    def test_model_query_get_entry(self):
        pass

    def test_model_query_add_entry_again(self):
        pass

    def test_model_query_get_entries(self):
        pass
