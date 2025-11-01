"""
OpenAI Response Generator
Handles generating natural language responses using OpenAI's API.
"""
from openai import OpenAI
from src import config
from typing import List, Dict, Any, Optional
from datetime import datetime


class ResponseGenerator:
    """Generates conversational responses using OpenAI's API."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        print("🤖 Initializing OpenAI Response Generator...")
        
        # Validate configuration
        config.validate_config()
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_API_BASE
        )
        self.model = config.OPENAI_MODEL
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = config.MAX_HISTORY_TURNS
        
        # System prompt for the chatbot
        self.system_prompt = """You are a helpful and friendly customer service chatbot. 
Your role is to assist users by answering their questions accurately and professionally.

Guidelines:
1. Use the provided knowledge base context to answer questions when available
2. If the context doesn't contain relevant information, politely say so and offer to help with something else
3. Be concise but thorough in your responses
4. Maintain a friendly and professional tone
5. If asked about topics outside the knowledge base, be honest about your limitations
6. Always prioritize accuracy over speculation

Remember: You have access to a knowledge base about business hours, account management, billing, security, technical support, and various services."""
        
        print(f"✅ Response Generator initialized with model: {self.model}")
    
    def generate_response(
        self, 
        user_query: str, 
        context: Optional[str] = None,
        include_history: bool = True
    ) -> str:
        """
        Generate a response to the user's query.
        
        Args:
            user_query: The user's question or message
            context: Relevant context from the knowledge base
            include_history: Whether to include conversation history
            
        Returns:
            Generated response text
        """
        try:
            # Build messages list
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if requested
            if include_history and self.conversation_history:
                # Limit history to max_history turns
                recent_history = self.conversation_history[-(self.max_history * 2):]
                messages.extend(recent_history)
            
            # Add context from knowledge base if available
            if context:
                context_message = f"""Based on the following information from our knowledge base, please answer the user's question:

{context}

Remember to synthesize this information naturally in your response. Don't just copy it verbatim."""
                messages.append({"role": "system", "content": context_message})
            
            # Add the current user query
            messages.append({"role": "user", "content": user_query})
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=0.7,
                max_tokens=500,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.3
            )
            
            # Extract response text
            assistant_response = response.choices[0].message.content
            if assistant_response is None:
                assistant_response = "I apologize, but I couldn't generate a response."
            else:
                assistant_response = assistant_response.strip()
            
            # Update conversation history
            self.add_to_history(user_query, assistant_response)
            
            return assistant_response
            
        except Exception as e:
            error_msg = f"I apologize, but I encountered an error: {str(e)}"
            print(f"❌ Error generating response: {e}")
            return error_msg
    
    def add_to_history(self, user_message: str, assistant_message: str):
        """
        Add a conversation turn to the history.
        
        Args:
            user_message: User's message
            assistant_message: Assistant's response
        """
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Trim history if it exceeds the maximum
        if len(self.conversation_history) > (self.max_history * 2):
            self.conversation_history = self.conversation_history[-(self.max_history * 2):]
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print("🗑️  Conversation history cleared")
    
    def get_history_summary(self) -> str:
        """Get a formatted summary of the conversation history."""
        if not self.conversation_history:
            return "No conversation history."
        
        summary = ["Conversation History:", "=" * 60]
        
        turn_number = 1
        for i in range(0, len(self.conversation_history), 2):
            if i + 1 < len(self.conversation_history):
                user_msg = self.conversation_history[i]['content']
                asst_msg = self.conversation_history[i + 1]['content']
                
                summary.append(f"\nTurn {turn_number}:")
                summary.append(f"User: {user_msg}")
                summary.append(f"Assistant: {asst_msg}")
                turn_number += 1
        
        summary.append("=" * 60)
        return "\n".join(summary)
    
    def save_conversation_log(self, filename: Optional[str] = None) -> Optional[str]:
        """
        Save the conversation history to a file.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to the saved log file
        """
        if not self.conversation_history:
            print("⚠️  No conversation to save.")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.txt"
        
        filepath = config.CONVERSATION_LOGS_PATH / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("CHATBOT CONVERSATION LOG\n")
                f.write("=" * 70 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Model: {self.model}\n")
                f.write(f"Total Turns: {len(self.conversation_history) // 2}\n")
                f.write("=" * 70 + "\n\n")
                
                turn_number = 1
                for i in range(0, len(self.conversation_history), 2):
                    if i + 1 < len(self.conversation_history):
                        user_msg = self.conversation_history[i]['content']
                        asst_msg = self.conversation_history[i + 1]['content']
                        
                        f.write(f"TURN {turn_number}\n")
                        f.write("-" * 70 + "\n")
                        f.write(f"User:\n{user_msg}\n\n")
                        f.write(f"Assistant:\n{asst_msg}\n")
                        f.write("-" * 70 + "\n\n")
                        turn_number += 1
                
                f.write("\n" + "=" * 70 + "\n")
                f.write("END OF CONVERSATION LOG\n")
            
            print(f"✅ Conversation log saved to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error saving conversation log: {e}")
            return None
    
    def set_system_prompt(self, new_prompt: str):
        """
        Update the system prompt.
        
        Args:
            new_prompt: New system prompt text
        """
        self.system_prompt = new_prompt
        print("✅ System prompt updated")
    
    def get_token_estimate(self) -> Dict[str, int]:
        """
        Get an estimate of tokens used in the current conversation.
        Note: This is a rough estimate (4 chars ≈ 1 token).
        
        Returns:
            Dictionary with token estimates
        """
        system_tokens = len(self.system_prompt) // 4
        history_text = " ".join([msg['content'] for msg in self.conversation_history])
        history_tokens = len(history_text) // 4
        
        return {
            'system_prompt': system_tokens,
            'conversation_history': history_tokens,
            'total_estimate': system_tokens + history_tokens,
            'turns': len(self.conversation_history) // 2
        }


def main():
    """Test the response generator."""
    print("\n" + "="*70)
    print("OpenAI Response Generator - Test Mode")
    print("="*70 + "\n")
    
    # Initialize generator
    generator = ResponseGenerator()
    
    # Test without context
    print("\n" + "-"*70)
    print("Test 1: Simple greeting (no context)")
    print("-"*70)
    query1 = "Hello! How are you today?"
    response1 = generator.generate_response(query1)
    print(f"User: {query1}")
    print(f"Assistant: {response1}")
    
    # Test with mock context
    print("\n" + "-"*70)
    print("Test 2: Question with context")
    print("-"*70)
    query2 = "What are your business hours?"
    context = """Question: What are your business hours?
Answer: Our business hours are Monday through Friday, 9:00 AM to 6:00 PM EST. We are closed on weekends and major holidays."""
    
    response2 = generator.generate_response(query2, context=context)
    print(f"User: {query2}")
    print(f"Assistant: {response2}")
    
    # Test follow-up (with history)
    print("\n" + "-"*70)
    print("Test 3: Follow-up question (with history)")
    print("-"*70)
    query3 = "Are you open on Saturdays?"
    response3 = generator.generate_response(query3, context=context)
    print(f"User: {query3}")
    print(f"Assistant: {response3}")
    
    # Show conversation history
    print("\n" + "-"*70)
    print("Conversation Summary")
    print("-"*70)
    print(generator.get_history_summary())
    
    # Show token estimate
    print("\n" + "-"*70)
    print("Token Usage Estimate")
    print("-"*70)
    token_info = generator.get_token_estimate()
    for key, value in token_info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Save conversation log
    print("\n" + "-"*70)
    print("Saving Conversation Log")
    print("-"*70)
    generator.save_conversation_log("test_conversation.txt")
    
    print("\n" + "="*70)
    print("✅ Response Generator test complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
