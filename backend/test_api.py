import unittest
from base import api, setup_mongo_client
from unittest.mock import patch, Mock 

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


    @patch("pymongo.collection.Collection.update_one")
    def test_register_success(self, mock_update_one):
        app_client = api.test_client()  # Create a test client for this test case

        # Mock the update_one method to simulate a successful registration
        mock_update_one.return_value = Mock(upserted_id=123)

        test_data = {
            'email': 'test_user',
            'password': 'test_password',
            'firstName': 'Test',
            'lastName': 'User'
        }

        response = app_client.post('/register', json=test_data)

        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertEqual(response_data['msg'], "register successful")

    def test_unauthorized_get_user_registered_events(self):
        # Mock the database query result
        app_client = api.test_client()

        db = app_client.application.mongo_client['test']  # Access the app's Mongo client
        collection = db['user']
        mock_find = Mock()

        collection.find = mock_find
        mock_find.return_value = [
            {"eventTitle": "Yoga"},
            {"eventTitle": "Swimming"}
        ]

        with patch("flask_jwt_extended.get_jwt_identity", return_value="test_user"):
            response = app_client.get('/usersEvents')

        self.assertEqual(response.status_code, 401)



if __name__ == "__main__":
    unittest.main()