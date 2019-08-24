import unittest

story = {
  "title": "Politics : NPR",
  "text": "Greenland, a Danish territory, has strategic value in terms of military activity and natural resources, said a member of Denmarks parliament. AP hide caption August 16, 2019 • NPR thanks our sponsors Become an NPR sponsor",
  "captions": [],
  "url": ["https://www.npr.org/series/tiny-desk-concerts/", "https://www.npr.org/sections/allsongs/", "https://www.npr.org/sections/music-news/", "https://www.npr.org/sections/music-features"],
  "origin": "https://www.npr.org/sections/politics/"
}

class TestModelContent(unittest.TestCase):

    def setUp(self):
        from artifice.scraper.foreground.models import db, Content
        self.db = db
        self.Content = Content
        self.story = story

    def tearDown(self):
        pass

    def test_model_content_db_is_empty(self):
        result = self.db.session.query(self.Content).all()
        self.assertFalse(result)
        # result <list> empty list return False

    def test_model_content_add_entry(self):
        from artifice.scraper.foreground.schemas import content_schema
        data, errors = content_schema.load(self.story)
        self.assertFalse(errors)
        self.db.session.add(data)
        self.db.session.commit()
        self.assertEqual(data.id, 1)

    def test_model_content_get_entry(self):
        pass

    def test_model_content_add_entry_again(self):
        pass

    def test_model_content_get_entries(self):
        pass
