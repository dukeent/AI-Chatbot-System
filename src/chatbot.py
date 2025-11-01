"""
Interactive Chatbot with ChromaDB, OpenAI, and Text-to-Speech
Main application that integrates all components.
"""
import sys
from datetime import datetime
from colorama import init, Fore, Style
from src import config
from src.knowledge_base import KnowledgeBase
from src.response_generator import ResponseGenerator
from src.tts_service import TTSService

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


class Chatbot:
    """Main chatbot class integrating all components."""
    
    def __init__(self, enable_tts: bool = True):
        """
        Initialize the chatbot with all required services.
        
        Args:
            enable_tts: Whether to enable text-to-speech functionality
        """
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "🤖 INTELLIGENT CHATBOT SYSTEM")
        print(Fore.CYAN + "="*70)
        print(Fore.YELLOW + "Initializing services...\n")
        
        try:
            # Validate configuration
            config.validate_config()
            
            # Initialize components
            self.knowledge_base = KnowledgeBase()
            self.response_generator = ResponseGenerator()
            
            # Initialize TTS (optional)
            self.enable_tts = enable_tts
            if enable_tts:
                self.tts_service = TTSService()
            else:
                self.tts_service = None
                print(Fore.YELLOW + "⚠️  TTS disabled")
            
            # Track conversation metadata
            self.conversation_start_time = datetime.now()
            self.total_queries = 0
            
            print(Fore.GREEN + "\n✅ All services initialized successfully!")
            
        except ValueError as e:
            print(Fore.RED + f"\n❌ Configuration Error: {e}")
            print(Fore.YELLOW + "\nPlease ensure you have:")
            print("1. Created a .env file from .env.example")
            print("2. Added your OpenAI API key to the .env file")
            sys.exit(1)
        except Exception as e:
            print(Fore.RED + f"\n❌ Initialization Error: {e}")
            sys.exit(1)
    
    def initialize_knowledge_base(self):
        """Load knowledge base data."""
        print(Fore.CYAN + "\n" + "-"*70)
        print(Fore.CYAN + "📚 Initializing Knowledge Base")
        print(Fore.CYAN + "-"*70)
        
        # Load FAQs
        count = self.knowledge_base.load_faqs_from_json()
        
        if count > 0:
            # Show statistics
            stats = self.knowledge_base.get_stats()
            print(Fore.GREEN + f"\n✅ Knowledge base ready with {stats['total_documents']} documents")
            
            if 'categories' in stats:
                print(Fore.CYAN + "\nCategories:")
                for category, doc_count in stats['categories'].items():
                    print(Fore.WHITE + f"  • {category}: {doc_count} documents")
        else:
            print(Fore.YELLOW + "⚠️  No documents loaded. Chatbot will work without knowledge base.")
    
    def process_query(self, user_query: str, enable_audio: bool = True) -> dict:
        """
        Process a user query through the full pipeline.
        
        Args:
            user_query: The user's question
            enable_audio: Whether to generate audio for this response
            
        Returns:
            Dictionary with response, context, and audio path
        """
        self.total_queries += 1
        
        # Step 1: Search knowledge base for relevant context
        print(Fore.CYAN + "\n🔍 Searching knowledge base...")
        search_results = self.knowledge_base.search(user_query)
        
        # Display search results
        if search_results['count'] > 0:
            print(Fore.GREEN + f"   Found {search_results['count']} relevant documents")
            for i, metadata in enumerate(search_results['metadatas'][:2], 1):
                relevance = 1 - search_results['distances'][i-1]
                print(Fore.WHITE + f"   • {metadata.get('category', 'N/A')} (relevance: {relevance:.2f})")
        else:
            print(Fore.YELLOW + "   No relevant documents found")
        
        # Step 2: Format context for LLM
        context = self.knowledge_base.format_context(search_results)
        
        # Step 3: Generate response using OpenAI
        print(Fore.CYAN + "🤖 Generating response...")
        response_text = self.response_generator.generate_response(
            user_query,
            context=context if search_results['count'] > 0 else None
        )
        
        # Step 4: Convert to speech (if enabled)
        audio_path = None
        if self.enable_tts and enable_audio and self.tts_service:
            print(Fore.CYAN + "🔊 Converting to speech...")
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_path = self.tts_service.text_to_speech(
                    response_text,
                    output_filename=f"response_{timestamp}.wav",
                    save_audio=True,
                    play_audio=False
                )
            except Exception as e:
                print(Fore.YELLOW + f"⚠️  TTS generation failed: {e}")
        
        return {
            'query': user_query,
            'response': response_text,
            'context': context,
            'audio_path': audio_path,
            'sources_found': search_results['count']
        }
    
    def run_interactive(self):
        """Run the chatbot in interactive CLI mode."""
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "💬 INTERACTIVE CHAT MODE")
        print(Fore.CYAN + "="*70)
        print(Fore.WHITE + "\nWelcome! I'm your intelligent assistant.")
        print(Fore.WHITE + "I can help you with questions about:")
        print(Fore.WHITE + "  • Business hours and general information")
        print(Fore.WHITE + "  • Account management and password resets")
        print(Fore.WHITE + "  • Billing, payments, and refunds")
        print(Fore.WHITE + "  • Security and data privacy")
        print(Fore.WHITE + "  • Technical support and integrations")
        
        print(Fore.YELLOW + "\nCommands:")
        print(Fore.WHITE + "  • Type your question and press Enter")
        print(Fore.WHITE + "  • 'quit' or 'exit' - End conversation")
        print(Fore.WHITE + "  • 'history' - View conversation history")
        print(Fore.WHITE + "  • 'clear' - Clear conversation history")
        print(Fore.WHITE + "  • 'stats' - View chatbot statistics")
        print(Fore.WHITE + "  • 'save' - Save conversation log")
        
        print(Fore.CYAN + "\n" + "-"*70 + "\n")
        
        while True:
            try:
                # Get user input
                user_input = input(Fore.GREEN + "You: " + Style.RESET_ALL).strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    self._handle_exit()
                    break
                
                elif user_input.lower() == 'history':
                    self._show_history()
                    continue
                
                elif user_input.lower() == 'clear':
                    self._clear_history()
                    continue
                
                elif user_input.lower() == 'stats':
                    self._show_statistics()
                    continue
                
                elif user_input.lower() == 'save':
                    self._save_conversation()
                    continue
                
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                # Process the query
                result = self.process_query(user_input)
                
                # Display response
                print(Fore.BLUE + "\nAssistant: " + Fore.WHITE + result['response'])
                
                if result['audio_path']:
                    print(Fore.CYAN + f"🔊 Audio: {result['audio_path']}")
                
                print(Fore.CYAN + "-"*70 + "\n")
                
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\n⚠️  Interrupted by user")
                self._handle_exit()
                break
            
            except Exception as e:
                print(Fore.RED + f"\n❌ Error: {e}")
                print(Fore.YELLOW + "Please try again or type 'quit' to exit.\n")
    
    def _handle_exit(self):
        """Handle graceful exit."""
        print(Fore.YELLOW + "\n👋 Thank you for chatting! Goodbye!\n")
        
        # Offer to save conversation
        if self.total_queries > 0:
            try:
                save = input(Fore.CYAN + "Save conversation log? (y/n): " + Style.RESET_ALL).strip().lower()
                if save == 'y':
                    self._save_conversation()
            except:
                pass
        
        # Show session summary
        self._show_session_summary()
    
    def _show_history(self):
        """Display conversation history."""
        print(Fore.CYAN + "\n" + "="*70)
        history = self.response_generator.get_history_summary()
        print(Fore.WHITE + history)
        print(Fore.CYAN + "="*70 + "\n")
    
    def _clear_history(self):
        """Clear conversation history."""
        self.response_generator.clear_history()
        print(Fore.GREEN + "✅ Conversation history cleared\n")
    
    def _show_statistics(self):
        """Display chatbot statistics."""
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "📊 CHATBOT STATISTICS")
        print(Fore.CYAN + "="*70)
        
        # Session info
        session_duration = datetime.now() - self.conversation_start_time
        print(Fore.WHITE + f"\nSession Duration: {session_duration}")
        print(Fore.WHITE + f"Total Queries: {self.total_queries}")
        
        # Token usage
        token_info = self.response_generator.get_token_estimate()
        print(Fore.WHITE + f"Conversation Turns: {token_info['turns']}")
        print(Fore.WHITE + f"Estimated Tokens: ~{token_info['total_estimate']}")
        
        # Knowledge base stats
        kb_stats = self.knowledge_base.get_stats()
        print(Fore.WHITE + f"\nKnowledge Base Documents: {kb_stats['total_documents']}")
        
        if 'categories' in kb_stats:
            print(Fore.WHITE + "Categories:")
            for category, count in kb_stats['categories'].items():
                print(Fore.WHITE + f"  • {category}: {count}")
        
        # TTS info
        if self.enable_tts and self.tts_service:
            tts_info = self.tts_service.get_model_info()
            print(Fore.WHITE + f"\nTTS Status: {tts_info.get('status', 'unknown')}")
        
        print(Fore.CYAN + "="*70 + "\n")
    
    def _save_conversation(self):
        """Save conversation log to file."""
        filepath = self.response_generator.save_conversation_log()
        if filepath:
            print(Fore.GREEN + f"✅ Conversation saved to: {filepath}\n")
    
    def _show_help(self):
        """Display help information."""
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "📖 HELP - Available Commands")
        print(Fore.CYAN + "="*70)
        print(Fore.WHITE + "\n  quit/exit    - End the conversation")
        print(Fore.WHITE + "  history      - View conversation history")
        print(Fore.WHITE + "  clear        - Clear conversation history")
        print(Fore.WHITE + "  stats        - View chatbot statistics")
        print(Fore.WHITE + "  save         - Save conversation log")
        print(Fore.WHITE + "  help         - Show this help message")
        print(Fore.CYAN + "="*70 + "\n")
    
    def _show_session_summary(self):
        """Display session summary on exit."""
        duration = datetime.now() - self.conversation_start_time
        
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + "📊 SESSION SUMMARY")
        print(Fore.CYAN + "="*70)
        print(Fore.WHITE + f"Duration: {duration}")
        print(Fore.WHITE + f"Queries Processed: {self.total_queries}")
        
        if self.total_queries > 0:
            token_info = self.response_generator.get_token_estimate()
            print(Fore.WHITE + f"Conversation Turns: {token_info['turns']}")
        
        print(Fore.CYAN + "="*70 + "\n")


def main():
    """Main entry point for the chatbot application."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive Chatbot with ChromaDB, OpenAI, and TTS")
    parser.add_argument('--no-tts', action='store_true', help='Disable text-to-speech')
    parser.add_argument('--no-kb', action='store_true', help='Skip knowledge base initialization')
    args = parser.parse_args()
    
    # Initialize chatbot
    chatbot = Chatbot(enable_tts=not args.no_tts)
    
    # Initialize knowledge base
    if not args.no_kb:
        chatbot.initialize_knowledge_base()
    
    # Run interactive mode
    chatbot.run_interactive()


if __name__ == "__main__":
    main()
