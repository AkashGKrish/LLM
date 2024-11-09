import unittest
from unittest.mock import patch
from chroma import setup_chromadb
import chromadb
class TestSetupChromaDB(unittest.TestCase):
    @patch('chromadb.PersistentClient')
    def test_create_collection(self, mock_client):
        collection_name = 'test_collection'
        setup_chromadb(collection_name)
        mock_client.assert_called_once_with(path="./chroma_data")
        mock_client.return_value.get_or_create_collection.assert_called_once_with(name=collection_name)
    @patch('chromadb.PersistentClient')
    def test_return_collection(self, mock_client):
        collection_name = 'test_collection'
        collection = setup_chromadb(collection_name)
        self.assertEqual(collection, mock_client.return_value.get_or_create_collection.return_value)
if __name__ == '__main__':
    unittest.main()