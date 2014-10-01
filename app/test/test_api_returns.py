import unittest
from app import app


class Testnextcall(unittest.TestCase):
    def test_api_response(self):
        self.app = app.test_client()
        response = self.app.get('/next/A', content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)