"""
ChromaDB Knowledge Base Manager
Handles storing and retrieving knowledge using vector embeddings.
"""
import json
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from src import config
from typing import List, Dict, Any, Optional
from pathlib import Path


class KnowledgeBase:
    """Manages the ChromaDB knowledge base for the chatbot."""
    
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        print("🔧 Initializing ChromaDB Knowledge Base...")
        
        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_PATH,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Use OpenAI embeddings for better semantic search
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=config.OPENAI_API_KEY,
            model_name=config.OPENAI_EMBEDDING_MODEL
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=config.COLLECTION_NAME
            )
            print(f"✅ Loaded existing collection '{config.COLLECTION_NAME}'")
            print(f"   Documents in collection: {self.collection.count()}")
        except Exception:
            self.collection = self.client.create_collection(
                name=config.COLLECTION_NAME,
                embedding_function=self.embedding_function,  # type: ignore
                metadata={"description": "FAQ and knowledge base for chatbot"}
            )
            print(f"✅ Created new collection '{config.COLLECTION_NAME}'")
    
    def load_faqs_from_json(self, filepath: Optional[str] = None, skip_prompt: bool = False) -> int:
        """
        Load FAQs from JSON file into ChromaDB.
        
        Args:
            filepath: Path to the JSON file containing FAQs
            skip_prompt: Skip the reload prompt (for web app)
            
        Returns:
            Number of FAQs loaded
        """
        if filepath is None:
            filepath = str(config.DATA_PATH / "faqs.json")
        
        print(f"📚 Loading FAQs from {filepath}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                faqs = json.load(f)
            
            # Check if collection already has data
            if self.collection.count() > 0:
                if skip_prompt:
                    print(f"ℹ️  Collection already contains {self.collection.count()} documents. Skipping reload.")
                    return self.collection.count()
                
                print(f"⚠️  Collection already contains {self.collection.count()} documents.")
                response = input("   Do you want to reset and reload? (y/n): ").strip().lower()
                if response == 'y':
                    self.reset_collection()
                else:
                    print("   Skipping load.")
                    return self.collection.count()
            
            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for faq in faqs:
                # Combine question and answer for better semantic search
                doc_text = f"Question: {faq['question']}\nAnswer: {faq['answer']}"
                documents.append(doc_text)
                
                metadatas.append({
                    "question": faq['question'],
                    "answer": faq['answer'],
                    "category": faq['category'],
                    "source": "faqs.json"
                })
                
                ids.append(faq['id'])
            
            # Add documents to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Successfully loaded {len(faqs)} FAQs into ChromaDB")
            return len(faqs)
            
        except FileNotFoundError:
            print(f"❌ Error: File not found at {filepath}")
            return 0
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON format - {e}")
            return 0
        except Exception as e:
            print(f"❌ Error loading FAQs: {e}")
            return 0
    
    def search(self, query: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """
        Search the knowledge base for relevant information.
        
        Args:
            query: User's question or query
            top_k: Number of results to return (default from config)
            
        Returns:
            Dictionary containing search results with documents, metadata, and distances
        """
        if top_k is None:
            top_k = config.TOP_K_RESULTS
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else [],
                'distances': results['distances'][0] if results['distances'] else [],
                'count': len(results['documents'][0]) if results['documents'] else 0
            }
            
        except Exception as e:
            print(f"❌ Error searching knowledge base: {e}")
            return {'documents': [], 'metadatas': [], 'distances': [], 'count': 0}
    
    def add_document(self, document: str, metadata: Dict[str, Any], doc_id: Optional[str] = None):
        """
        Add a single document to the knowledge base.
        
        Args:
            document: Text content to add
            metadata: Metadata dictionary for the document
            doc_id: Unique identifier (auto-generated if not provided)
        """
        import uuid
        
        if doc_id is None:
            doc_id = f"doc_{uuid.uuid4().hex[:8]}"
        
        try:
            self.collection.add(
                documents=[document],
                metadatas=[metadata],
                ids=[doc_id]
            )
            print(f"✅ Added document with ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Error adding document: {e}")
            return None
    
    def get_all_documents(self) -> Dict[str, Any]:
        """Get all documents from the collection."""
        try:
            results = self.collection.get()
            return {
                'ids': results['ids'],
                'documents': results['documents'],
                'metadatas': results['metadatas'],
                'count': len(results['ids'])
            }
        except Exception as e:
            print(f"❌ Error retrieving documents: {e}")
            return {'ids': [], 'documents': [], 'metadatas': [], 'count': 0}
    
    def reset_collection(self):
        """Reset the collection by deleting and recreating it."""
        try:
            self.client.delete_collection(name=config.COLLECTION_NAME)
            self.collection = self.client.create_collection(
                name=config.COLLECTION_NAME,
                embedding_function=self.embedding_function,  # type: ignore
                metadata={"description": "FAQ and knowledge base for chatbot"}
            )
            print(f"✅ Collection '{config.COLLECTION_NAME}' has been reset")
        except Exception as e:
            print(f"❌ Error resetting collection: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        count = self.collection.count()
        
        stats = {
            'total_documents': count,
            'collection_name': config.COLLECTION_NAME,
            'embedding_model': config.OPENAI_EMBEDDING_MODEL
        }
        
        if count > 0:
            # Get category distribution
            all_docs = self.get_all_documents()
            categories = {}
            for metadata in all_docs['metadatas']:
                category = metadata.get('category', 'unknown')
                categories[category] = categories.get(category, 0) + 1
            stats['categories'] = categories
        
        return stats
    
    def format_context(self, search_results: Dict[str, Any]) -> str:
        """
        Format search results into a context string for the LLM.
        
        Args:
            search_results: Results from the search method
            
        Returns:
            Formatted context string
        """
        if search_results['count'] == 0:
            return "No relevant information found in the knowledge base."
        
        context_parts = ["Here is relevant information from the knowledge base:\n"]
        
        for i, (doc, metadata, distance) in enumerate(zip(
            search_results['documents'],
            search_results['metadatas'],
            search_results['distances']
        ), 1):
            context_parts.append(f"\n[Source {i} - Relevance: {1 - distance:.2f}]")
            context_parts.append(f"Category: {metadata.get('category', 'N/A')}")
            context_parts.append(f"Q: {metadata.get('question', 'N/A')}")
            context_parts.append(f"A: {metadata.get('answer', 'N/A')}")
        
        return "\n".join(context_parts)


def main():
    """Test the knowledge base functionality."""
    print("\n" + "="*60)
    print("ChromaDB Knowledge Base - Test Mode")
    print("="*60 + "\n")
    
    # Validate configuration
    try:
        config.validate_config()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        return
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    
    # Load FAQs
    kb.load_faqs_from_json()
    
    # Display statistics
    print("\n" + "-"*60)
    print("📊 Knowledge Base Statistics:")
    print("-"*60)
    stats = kb.get_stats()
    for key, value in stats.items():
        if key == 'categories':
            print(f"\n{key.replace('_', ' ').title()}:")
            for cat, count in value.items():
                print(f"  - {cat}: {count}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Test search
    print("\n" + "-"*60)
    print("🔍 Testing Search Functionality")
    print("-"*60)
    
    test_queries = [
        "How do I reset my password?",
        "What payment methods are available?",
        "Is my data secure?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = kb.search(query, top_k=2)
        
        if results['count'] > 0:
            print(f"Found {results['count']} relevant results:")
            for i, metadata in enumerate(results['metadatas'], 1):
                print(f"\n  Result {i}:")
                print(f"  Question: {metadata['question']}")
                print(f"  Category: {metadata['category']}")
                print(f"  Relevance: {1 - results['distances'][i-1]:.3f}")
        else:
            print("No results found.")
    
    print("\n" + "="*60)
    print("✅ Knowledge Base test complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
