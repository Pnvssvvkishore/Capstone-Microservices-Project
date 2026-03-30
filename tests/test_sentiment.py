import unittest
from unittest.mock import patch, MagicMock
from flask import json
import os
import sys

# Add the sentiment-service to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sentiment-service')))

from app import app

class TestSentiment(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_positive_sentiment(self):
        """Test 'POSITIVE' sentiment analysis with a known positive string"""
        response = self.app.post('/analyze', 
                                json={"text": "I absolutely love this amazing product!"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['sentiment'], 'POSITIVE')

    def test_negative_sentiment(self):
        """Test 'NEGATIVE' sentiment analysis with a known negative string"""
        response = self.app.post('/analyze', 
                                json={"text": "This is the worst and most broken thing ever!"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['sentiment'], 'NEGATIVE')

    def test_neutral_sentiment(self):
        """Test 'NEUTRAL' sentiment analysis with a neutral string"""
        response = self.app.post('/analyze', 
                                json={"text": "This is a product which exists."})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['sentiment'], 'NEUTRAL')

    def test_empty_text(self):
        """Test analysis with empty text returns 400 Bad Request"""
        response = self.app.post('/analyze', json={"text": ""})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'No text provided')

if __name__ == '__main__':
    unittest.main()
