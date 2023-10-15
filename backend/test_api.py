import unittest
from base import api, setup_mongo_client
from unittest.mock import Mock

class APITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = api
        self.app.config['TESTING'] = True
        setup_mongo_client(self.app)  # Set up the mongo client after changing the TESTING flag
        self.client = self.app.test_client()
        print("Using MongoDB client:", type(self.app.mongo_client)) 

    
    def test_get_events(self):
        # Create a mock collection
        db = self.app.mongo_client['test']
        collection = db['events']

        # Replace the collection's find method with a Mock object
        mock_find = Mock()
        collection.find = mock_find
        mock_find.return_value = [
            {"_id": "Event 1"},
            {"_id": "Event 2"},
        ]

        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()