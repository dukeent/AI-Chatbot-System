"""
Example usage demonstrations for the chatbot system.
Shows various ways to use the chatbot components.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config
from src.knowledge_base import KnowledgeBase
from src.response_generator import ResponseGenerator
from src.tts_service import TTSService
from src.chatbot import Chatbot


def example_1_knowledge_base():
    """Example: Using the knowledge base directly."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Knowledge Base Usage")
    print("="*70 + "\n")
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    kb.load_faqs_from_json()
    
    # Search for information
    queries = [
        "How do I reset my password?",
        "What payment methods do you accept?",
        "Is my data secure?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        results = kb.search(query, top_k=2)
        
        print(f"Found {results['count']} relevant documents:")
        for i, (metadata, distance) in enumerate(zip(results['metadatas'], results['distances']), 1):
            print(f"\n  Result {i}:")
            print(f"  Question: {metadata['question']}")
            print(f"  Answer: {metadata['answer'][:100]}...")
            print(f"  Relevance: {1 - distance:.3f}")


def example_2_response_generation():
    """Example: Generating responses with context."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Response Generation")
    print("="*70 + "\n")
    
    # Initialize components
    kb = KnowledgeBase()
    kb.load_faqs_from_json()
    rg = ResponseGenerator()
    
    # Query with context
    query = "How can I contact support?"
    
    print(f"Query: {query}\n")
    
    # Get context from knowledge base
    search_results = kb.search(query)
    context = kb.format_context(search_results)
    
    # Generate response
    response = rg.generate_response(query, context)
    
    print(f"Response: {response}")


def example_3_multi_turn_conversation():
    """Example: Multi-turn conversation with history."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Multi-turn Conversation")
    print("="*70 + "\n")
    
    # Initialize components
    kb = KnowledgeBase()
    kb.load_faqs_from_json()
    rg = ResponseGenerator()
    
    # Conversation turns
    conversation = [
        "What are your business hours?",
        "Are you open on weekends?",
        "How can I contact you outside business hours?"
    ]
    
    for i, query in enumerate(conversation, 1):
        print(f"\nTurn {i}")
        print(f"User: {query}")
        
        # Get context and generate response
        search_results = kb.search(query)
        context = kb.format_context(search_results)
        response = rg.generate_response(query, context)
        
        print(f"Assistant: {response}")
    
    # Show conversation history
    print("\n" + "-"*70)
    print("Conversation History:")
    print(rg.get_history_summary())


def example_4_text_to_speech():
    """Example: Converting text to speech."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Text-to-Speech")
    print("="*70 + "\n")
    
    # Initialize TTS
    tts = TTSService()
    
    # Sample responses to convert
    texts = [
        "Hello! How can I help you today?",
        "Our business hours are Monday through Friday, 9 AM to 6 PM.",
        "Thank you for contacting us. Have a great day!"
    ]
    
    print("Converting texts to speech...\n")
    
    for i, text in enumerate(texts, 1):
        print(f"{i}. {text}")
        audio_path = tts.text_to_speech(
            text,
            output_filename=f"example_{i}.wav"
        )
        if audio_path:
            print(f"   ✓ Audio saved: {audio_path}\n")


def example_5_full_pipeline():
    """Example: Complete chatbot pipeline."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Full Chatbot Pipeline")
    print("="*70 + "\n")
    
    # Initialize chatbot
    chatbot = Chatbot(enable_tts=True)
    chatbot.initialize_knowledge_base()
    
    # Process queries
    queries = [
        "What payment methods do you accept?",
        "Can I get a refund?",
        "How do I reset my password?"
    ]
    
    for query in queries:
        print(f"\n{'='*70}")
        print(f"Processing: {query}")
        print('='*70)
        
        result = chatbot.process_query(query, enable_audio=True)
        
        print(f"\nResponse: {result['response']}")
        print(f"Sources found: {result['sources_found']}")
        
        if result['audio_path']:
            print(f"Audio: {result['audio_path']}")


def example_6_batch_operations():
    """Example: Batch processing operations."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Batch Operations")
    print("="*70 + "\n")
    
    # Initialize services
    tts = TTSService()
    
    # Batch TTS conversion
    responses = [
        "Welcome to our service!",
        "Your account has been created successfully.",
        "Thank you for your feedback.",
        "Your request has been processed."
    ]
    
    print("Batch converting responses to speech...\n")
    audio_files = tts.batch_convert(responses, prefix="batch_example")
    
    print(f"\nGenerated {len(audio_files)} audio files:")
    for audio_file in audio_files:
        print(f"  • {audio_file}")


def example_7_custom_knowledge():
    """Example: Adding custom knowledge to the database."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Custom Knowledge Addition")
    print("="*70 + "\n")
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    kb.load_faqs_from_json()
    
    # Add custom document
    custom_doc = """
    Question: What is the chatbot workshop about?
    Answer: The chatbot workshop teaches participants how to build a complete chatbot system 
    using ChromaDB for knowledge storage, OpenAI for natural language generation, and 
    HuggingFace Text-to-Speech for audio responses.
    """
    
    metadata = {
        "question": "What is the chatbot workshop about?",
        "answer": "The workshop teaches building chatbots with ChromaDB, OpenAI, and HuggingFace TTS.",
        "category": "workshop",
        "source": "custom"
    }
    
    print("Adding custom knowledge...")
    doc_id = kb.add_document(custom_doc, metadata)
    
    # Search for it
    print("\nSearching for custom knowledge...")
    results = kb.search("Tell me about the workshop")
    
    if results['count'] > 0:
        print(f"\nFound {results['count']} results:")
        for metadata in results['metadatas']:
            if metadata.get('source') == 'custom':
                print(f"\n✓ Custom knowledge retrieved!")
                print(f"  Category: {metadata['category']}")
                print(f"  Answer: {metadata['answer']}")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("CHATBOT SYSTEM - USAGE EXAMPLES")
    print("="*70)
    
    examples = [
        ("Knowledge Base Search", example_1_knowledge_base),
        ("Response Generation", example_2_response_generation),
        ("Multi-turn Conversation", example_3_multi_turn_conversation),
        ("Text-to-Speech", example_4_text_to_speech),
        ("Full Pipeline", example_5_full_pipeline),
        ("Batch Operations", example_6_batch_operations),
        ("Custom Knowledge", example_7_custom_knowledge)
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nOptions:")
    print("  • Enter a number (1-7) to run a specific example")
    print("  • Enter 'all' to run all examples")
    print("  • Enter 'quit' to exit")
    
    while True:
        try:
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == 'quit':
                print("\nGoodbye!")
                break
            
            elif choice == 'all':
                for name, func in examples:
                    try:
                        func()
                        input("\nPress Enter to continue...")
                    except Exception as e:
                        print(f"\n❌ Error in {name}: {e}")
                break
            
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(examples):
                    name, func = examples[idx]
                    try:
                        func()
                    except Exception as e:
                        print(f"\n❌ Error: {e}")
                else:
                    print("Invalid choice. Please enter 1-7.")
            else:
                print("Invalid choice. Please enter a number, 'all', or 'quit'.")
                
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Validate configuration first
    try:
        config.validate_config()
        main()
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure:")
        print("1. You have a .env file (copy from .env.example)")
        print("2. Your OPENAI_API_KEY is set in the .env file")
