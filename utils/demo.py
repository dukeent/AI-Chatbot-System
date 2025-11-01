"""
Offline Demo - Demonstrates chatbot architecture without API calls
Useful for understanding the system flow without needing API keys
"""
from datetime import datetime
from colorama import init, Fore, Style
import json
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize colorama
init(autoreset=True)


class MockKnowledgeBase:
    """Mock knowledge base for demonstration."""
    
    def __init__(self):
        self.documents = []
        print(Fore.GREEN + "✅ Mock Knowledge Base initialized")
    
    def load_faqs(self, filepath="data/faqs.json"):
        """Load FAQs from JSON file."""
        try:
            with open(filepath, 'r') as f:
                self.documents = json.load(f)
            print(Fore.GREEN + f"✅ Loaded {len(self.documents)} FAQs")
            return len(self.documents)
        except Exception as e:
            print(Fore.RED + f"❌ Error loading FAQs: {e}")
            return 0
    
    def search(self, query):
        """Simple keyword-based search (mock)."""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            # Simple keyword matching
            if any(word in doc['question'].lower() or word in doc['answer'].lower() 
                   for word in query_lower.split()):
                results.append(doc)
        
        # Limit to top 3
        return results[:3]


class MockResponseGenerator:
    """Mock response generator for demonstration."""
    
    def __init__(self):
        self.conversation_history = []
        print(Fore.GREEN + "✅ Mock Response Generator initialized")
    
    def generate_response(self, query, context_docs):
        """Generate a simple response based on context."""
        if context_docs:
            # Use the most relevant document
            doc = context_docs[0]
            response = f"{doc['answer']}\n\nThis information is from our {doc['category']} knowledge base."
        else:
            response = "I apologize, but I don't have specific information about that in my knowledge base. However, I'm here to help! Could you rephrase your question or ask about something else?"
        
        self.conversation_history.append({
            'query': query,
            'response': response,
            'timestamp': datetime.now()
        })
        
        return response


class MockTTSService:
    """Mock TTS service for demonstration."""
    
    def __init__(self):
        self.audio_count = 0
        print(Fore.GREEN + "✅ Mock TTS Service initialized")
    
    def text_to_speech(self, text):
        """Simulate TTS generation."""
        self.audio_count += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mock_path = f"audio_responses/response_{timestamp}.wav"
        
        # Simulate file creation
        print(Fore.CYAN + f"   [Simulated] Audio would be saved to: {mock_path}")
        print(Fore.CYAN + f"   [Simulated] Audio length: ~{len(text.split())/2:.1f} seconds")
        
        return mock_path


class DemoChatbot:
    """Demo chatbot that works without API keys."""
    
    def __init__(self):
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "🤖 CHATBOT DEMO - OFFLINE MODE")
        print(Fore.CYAN + "="*70)
        print(Fore.YELLOW + "\n⚠️  Running in DEMO mode (no API calls required)")
        print(Fore.WHITE + "This demonstrates the chatbot architecture without needing API keys.\n")
        
        self.kb = MockKnowledgeBase()
        self.rg = MockResponseGenerator()
        self.tts = MockTTSService()
        
        self.total_queries = 0
        self.start_time = datetime.now()
    
    def initialize(self):
        """Initialize the knowledge base."""
        print(Fore.CYAN + "\n📚 Loading Knowledge Base...")
        count = self.kb.load_faqs()
        
        if count > 0:
            print(Fore.GREEN + f"✅ Knowledge base ready with {count} documents\n")
            return True
        return False
    
    def process_query(self, query):
        """Process a user query."""
        self.total_queries += 1
        
        print(Fore.CYAN + "\n" + "-"*70)
        print(Fore.GREEN + f"User: {query}")
        print(Fore.CYAN + "-"*70)
        
        # Step 1: Search knowledge base
        print(Fore.CYAN + "\n🔍 Step 1: Searching knowledge base...")
        results = self.kb.search(query)
        
        if results:
            print(Fore.GREEN + f"   Found {len(results)} relevant documents:")
            for i, doc in enumerate(results, 1):
                print(Fore.WHITE + f"   {i}. Category: {doc['category']} - {doc['question']}")
        else:
            print(Fore.YELLOW + "   No relevant documents found")
        
        # Step 2: Generate response
        print(Fore.CYAN + "\n🤖 Step 2: Generating response...")
        response = self.rg.generate_response(query, results)
        print(Fore.BLUE + f"\nAssistant: {response}")
        
        # Step 3: Convert to speech
        print(Fore.CYAN + "\n🔊 Step 3: Converting to speech...")
        audio_path = self.tts.text_to_speech(response)
        
        print(Fore.CYAN + "\n" + "-"*70 + "\n")
        
        return response
    
    def run_demo(self):
        """Run an automated demo."""
        if not self.initialize():
            print(Fore.RED + "Failed to initialize. Exiting.")
            return
        
        # Demo queries
        demo_queries = [
            "What are your business hours?",
            "How do I reset my password?",
            "What payment methods do you accept?",
            "Is my data secure?",
            "Can I get a refund?"
        ]
        
        print(Fore.CYAN + "="*70)
        print(Fore.CYAN + "RUNNING AUTOMATED DEMO")
        print(Fore.CYAN + "="*70)
        print(Fore.WHITE + "\nProcessing 5 sample queries...\n")
        
        for i, query in enumerate(demo_queries, 1):
            print(Fore.YELLOW + f"\n{'='*70}")
            print(Fore.YELLOW + f"QUERY {i}/{len(demo_queries)}")
            print(Fore.YELLOW + f"{'='*70}")
            
            self.process_query(query)
            
            if i < len(demo_queries):
                input(Fore.CYAN + "Press Enter to continue to next query...")
        
        self.show_summary()
    
    def run_interactive(self):
        """Run in interactive mode."""
        if not self.initialize():
            print(Fore.RED + "Failed to initialize. Exiting.")
            return
        
        print(Fore.CYAN + "="*70)
        print(Fore.CYAN + "INTERACTIVE DEMO MODE")
        print(Fore.CYAN + "="*70)
        print(Fore.WHITE + "\nType your questions (or 'quit' to exit)\n")
        
        while True:
            try:
                query = input(Fore.GREEN + "You: " + Style.RESET_ALL).strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit', 'bye']:
                    print(Fore.YELLOW + "\n👋 Goodbye!")
                    break
                
                if query.lower() == 'summary':
                    self.show_summary()
                    continue
                
                self.process_query(query)
                
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\n⚠️  Interrupted by user. Goodbye!")
                break
    
    def show_summary(self):
        """Show demo summary."""
        duration = datetime.now() - self.start_time
        
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "📊 DEMO SUMMARY")
        print(Fore.CYAN + "="*70)
        print(Fore.WHITE + f"\nTotal Queries: {self.total_queries}")
        print(Fore.WHITE + f"Session Duration: {duration}")
        print(Fore.WHITE + f"Knowledge Base Size: {len(self.kb.documents)} documents")
        print(Fore.WHITE + f"Conversation Turns: {len(self.rg.conversation_history)}")
        print(Fore.WHITE + f"Audio Files Generated: {self.tts.audio_count} (simulated)")
        
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.GREEN + "✅ Demo completed successfully!")
        print(Fore.CYAN + "="*70)
        
        print(Fore.YELLOW + "\n📝 Note: This was a demonstration mode.")
        print(Fore.WHITE + "To use the actual chatbot with API integration:")
        print(Fore.WHITE + "  1. Configure your .env file with OPENAI_API_KEY")
        print(Fore.WHITE + "  2. Run: python chatbot.py")
        print(Fore.CYAN + "="*70 + "\n")


def show_architecture():
    """Display system architecture."""
    print(Fore.CYAN + "\n" + "="*70)
    print(Fore.CYAN + "🏗️  CHATBOT SYSTEM ARCHITECTURE")
    print(Fore.CYAN + "="*70)
    
    print(Fore.WHITE + """
    ┌─────────────────────────────────────────────────────────────┐
    │                    USER INTERFACE (CLI)                      │
    └─────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                   CHATBOT CONTROLLER                         │
    │  • Orchestrates all components                               │
    │  • Manages conversation flow                                 │
    │  • Handles user commands                                     │
    └─────────────────────────────────────────────────────────────┘
                    │              │              │
            ┌───────┘              │              └───────┐
            ▼                      ▼                      ▼
    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
    │  CHROMADB    │      │   OPENAI     │      │ HUGGINGFACE  │
    │  (Knowledge) │      │  (Response)  │      │    (TTS)     │
    └──────────────┘      └──────────────┘      └──────────────┘
            │                      │                      │
            ▼                      ▼                      ▼
    • Vector Search      • GPT Models        • VITS Model
    • Embeddings         • Chat Completion   • Audio Gen
    • Similarity         • Context Aware     • WAV Files
    
    """)
    
    print(Fore.CYAN + "="*70 + "\n")


def main():
    """Main demo entry point."""
    print(Fore.CYAN + "\n" + "="*70)
    print(Fore.CYAN + "CHATBOT SYSTEM - OFFLINE DEMO")
    print(Fore.CYAN + "="*70)
    
    print(Fore.WHITE + "\nDemo Options:")
    print(Fore.WHITE + "  1. Show System Architecture")
    print(Fore.WHITE + "  2. Run Automated Demo (5 sample queries)")
    print(Fore.WHITE + "  3. Run Interactive Demo (ask your own questions)")
    print(Fore.WHITE + "  4. Exit")
    
    while True:
        try:
            choice = input(Fore.GREEN + "\nYour choice (1-4): " + Style.RESET_ALL).strip()
            
            if choice == '1':
                show_architecture()
            
            elif choice == '2':
                chatbot = DemoChatbot()
                chatbot.run_demo()
                break
            
            elif choice == '3':
                chatbot = DemoChatbot()
                chatbot.run_interactive()
                break
            
            elif choice == '4':
                print(Fore.YELLOW + "\nGoodbye!")
                break
            
            else:
                print(Fore.RED + "Invalid choice. Please enter 1-4.")
        
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\nInterrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()
