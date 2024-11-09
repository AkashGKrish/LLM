import unittest
from unittest.mock import patch, MagicMock
from kgConnection import upload_to_fuseki
from rdflib import Graph
import requests

class TestUploadToFuseki(unittest.TestCase):

    @patch('requests.put')
    def test_successful_upload(self, mock_put):
        mock_put.return_value.status_code = 200
        file_path = 'test.ttl'
        fuseki_url = 'http://example.com/fuseki'
        self.assertTrue(upload_to_fuseki(file_path, fuseki_url))

    @patch('rdflib.Graph.parse')
    def test_invalid_file_path(self, mock_parse):
        mock_parse.side_effect = FileNotFoundError
        file_path = 'invalid_file_path.ttl'
        fuseki_url = 'http://example.com/fuseki'
        self.assertFalse(upload_to_fuseki(file_path, fuseki_url))

    @patch('requests.put')
    def test_invalid_fuseki_url(self, mock_put):
        mock_put.side_effect = requests.exceptions.RequestException
        file_path = 'test.ttl'
        fuseki_url = 'http://invalid_url.com/fuseki'
        self.assertFalse(upload_to_fuseki(file_path, fuseki_url))

    def test_unsupported_file_format(self):
        file_path = 'test.rdf'
        fuseki_url = 'http://example.com/fuseki'
        self.assertFalse(upload_to_fuseki(file_path, fuseki_url, format='rdf'))

    @patch('rdflib.Graph.parse')
    def test_exception_handling(self, mock_parse):
        mock_parse.side_effect = Exception('Test exception')
        file_path = 'test.ttl'
        fuseki_url = 'http://example.com/fuseki'
        self.assertFalse(upload_to_fuseki(file_path, fuseki_url))

if __name__ == '__main__':
    unittest.main()