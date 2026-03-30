import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add the api-gateway directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api-gateway')))

# Set dummy environment variables NOT to require a real Redis or service for basic testing
os.environ['SECRET_KEY'] = 'test_secret'
os.environ['USER_SERVICE_URL'] = 'http://test-user'
os.environ['PRODUCT_SERVICE_URL'] = 'http://test-product'

# Importing the app from api-gateway
from app import app

class TestGateway(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        """Test the root (/) endpoint returns 200 OK"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'API Gateway is running')

    @patch('requests.request')
    def test_get_products_proxy(self, mock_request):
        """Test the /products proxy route works correctly with a mock response"""
        # Mocking the Product Service response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Test Laptop", "price": 999.0}]
        mock_request.return_value = mock_response

        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Laptop')
        
        # Verify it called the correct internal service URL
        args, kwargs = mock_request.call_args
        self.assertIn('http://test-product/products', args[1])

if __name__ == '__main__':
    unittest.main()
