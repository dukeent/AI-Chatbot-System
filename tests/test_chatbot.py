"""
Test suite for the chatbot system.
Tests individual components and integration.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config
from src.knowledge_base import KnowledgeBase
from src.response_generator import ResponseGenerator


class TestKnowledgeBase(unittest.TestCase):
    """Test cases for ChromaDB knowledge base."""
    
    @patch('knowledge_base.chromadb.PersistentClient')
    @patch('knowledge_base.embedding_functions.OpenAIEmbeddingFunction')
    def test_initialization(self, mock_embedding, mock_client):
        """Test knowledge base initialization."""
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.return_value.create_collection.return_value = mock_collection
        
        kb = KnowledgeBase()
        self.assertIsNotNone(kb)
        self.assertEqual(kb.collection.count(), 0)
    
    def test_format_context(self):
        """Test context formatting."""
        kb = KnowledgeBase()
        
        search_results = {
            'documents': ['Doc 1', 'Doc 2'],
            'metadatas': [
                {'question': 'Q1', 'answer': 'A1', 'category': 'test'},
                {'question': 'Q2', 'answer': 'A2', 'category': 'test'}
            ],
            'distances': [0.1, 0.2],
            'count': 2
        }
        
        context = kb.format_context(search_results)
        self.assertIn('Source 1', context)
        self.assertIn('Source 2', context)
        self.assertIn('Q1', context)
        self.assertIn('A1', context)


class TestResponseGenerator(unittest.TestCase):
    """Test cases for OpenAI response generator."""
    
    @patch('response_generator.OpenAI')
    @patch('config.validate_config')
    def test_initialization(self, mock_validate, mock_openai):
        """Test response generator initialization."""
        mock_validate.return_value = True
        
        rg = ResponseGenerator()
        self.assertIsNotNone(rg)
        self.assertEqual(len(rg.conversation_history), 0)
    
    @patch('response_generator.OpenAI')
    @patch('config.validate_config')
    def test_add_to_history(self, mock_validate, mock_openai):
        """Test adding messages to conversation history."""
        mock_validate.return_value = True
        
        rg = ResponseGenerator()
        rg.add_to_history("Hello", "Hi there!")
        
        self.assertEqual(len(rg.conversation_history), 2)
        self.assertEqual(rg.conversation_history[0]['role'], 'user')
        self.assertEqual(rg.conversation_history[1]['role'], 'assistant')
    
    @patch('response_generator.OpenAI')
    @patch('config.validate_config')
    def test_clear_history(self, mock_validate, mock_openai):
        """Test clearing conversation history."""
        mock_validate.return_value = True
        
        rg = ResponseGenerator()
        rg.add_to_history("Test", "Response")
        rg.clear_history()
        
        self.assertEqual(len(rg.conversation_history), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for the full chatbot pipeline."""
    
    @patch('knowledge_base.chromadb.PersistentClient')
    @patch('knowledge_base.embedding_functions.OpenAIEmbeddingFunction')
    @patch('response_generator.OpenAI')
    @patch('config.validate_config')
    def test_query_pipeline(self, mock_validate, mock_openai, mock_embedding, mock_client):
        """Test the full query processing pipeline."""
        mock_validate.return_value = True
        
        # Mock ChromaDB
        mock_collection = MagicMock()
        mock_collection.count.return_value = 5
        mock_collection.query.return_value = {
            'documents': [['Test doc']],
            'metadatas': [[{'question': 'Q', 'answer': 'A', 'category': 'test'}]],
            'distances': [[0.1]]
        }
        mock_client.return_value.create_collection.return_value = mock_collection
        
        # Mock OpenAI
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_completion
        
        # Test pipeline
        kb = KnowledgeBase()
        rg = ResponseGenerator()
        
        # Search
        results = kb.search("test query")
        self.assertEqual(results['count'], 1)
        
        # Format context
        context = kb.format_context(results)
        self.assertIn('Test doc', context)
        
        # Generate response
        response = rg.generate_response("test query", context)
        self.assertEqual(response, "Test response")


def run_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("🧪 RUNNING UNIT TESTS")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeBase))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
