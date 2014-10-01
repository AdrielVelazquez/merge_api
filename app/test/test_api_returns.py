import unittest
import couchdb
from app import app
import uuid

RANDOM_HASH = uuid.uuid4().hex[:5]
server = couchdb.Server()

class Testnextcall(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print "Building Databases and Creating MockData"
        db = server.create("test_" + RANDOM_HASH)
        def create_mock_data(db):
            db.update([{"_id": "A", "list": [2, 3, 8], "idx": 0}, {"_id": "B", "list": [4, 5, 6], "idx": 0}])
            db.update([{"_id": "merge"}])

        self.data = create_mock_data(db=db)


    @classmethod
    def tearDownClass(cls):
        print "Tearing Down"
        del server["test_" + RANDOM_HASH]

    def test_api_response(self):
        self.app = app.test_client()
        response = self.app.get('/quiz/next/A', content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)