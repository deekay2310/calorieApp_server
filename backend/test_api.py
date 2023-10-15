import unittest
import mongomock
from base import api
from unittest.mock import patch, Mock

class APITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = api
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    
    def test_get_events(self):
        with patch('pymongo.MongoClient') as mock_mongo_client:
            # Create a mock MongoClient instance
            mock_mongo = mongomock.MongoClient()
            mock_mongo_client.return_value = mock_mongo

            # Create a mock collection
            mock_db = mock_mongo['test']
            mock_collection = mock_db['events']

            # Mock the find method on the collection
            mock_collection.find = Mock()
            mock_collection.find.return_value = [
                {"name": "Event 1"},
                {"name": "Event 2"},
            ]

            response = self.client.get('/events')
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()