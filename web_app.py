"""
Flask Web Application for Chatbot
Provides a web-based interface for the intelligent chatbot.
"""
from flask import Flask, render_template, request, jsonify, send_file
from src.knowledge_base import KnowledgeBase
from src.response_generator import ResponseGenerator
from src.tts_service import TTSService
from src import config
from datetime import datetime
from pathlib import Path
import os

app = Flask(__name__)

# Initialize chatbot components
print("🚀 Initializing Chatbot Web Application...")
knowledge_base = KnowledgeBase()
response_generator = ResponseGenerator()
tts_service = TTSService()

# Load FAQs
print("📚 Loading knowledge base...")
knowledge_base.load_faqs_from_json(skip_prompt=True)

# Statistics tracking
session_stats = {
    'total_queries': 0,
    'start_time': datetime.now()
}


@app.route('/')
def home():
    """Render the main chat interface."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the user.
    
    Expected JSON:
        {
            "message": "user's question",
            "enable_audio": true/false
        }
    
    Returns:
        {
            "response": "chatbot response",
            "audio_url": "/audio/response_xyz.wav" (if audio enabled),
            "sources_found": 2,
            "timestamp": "2025-11-01 10:30:45"
        }
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        enable_audio = data.get('enable_audio', True)
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Update statistics
        session_stats['total_queries'] += 1
        
        # Search knowledge base
        search_results = knowledge_base.search(user_message)
        context = knowledge_base.format_context(search_results) if search_results['count'] > 0 else None
        
        # Generate response
        response_text = response_generator.generate_response(
            user_message,
            context=context
        )
        
        # Generate audio if enabled
        audio_url = None
        if enable_audio:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = tts_service.text_to_speech(
                response_text,
                output_filename=f"response_{timestamp}.wav",
                save_audio=True,
                play_audio=False
            )
            if audio_path:
                audio_filename = Path(audio_path).name
                audio_url = f"/audio/{audio_filename}"
        
        return jsonify({
            'response': response_text,
            'audio_url': audio_url,
            'sources_found': search_results['count'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        print(f"❌ Error processing chat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history."""
    try:
        response_generator.clear_history()
        return jsonify({'message': 'Conversation history cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get chatbot statistics."""
    try:
        kb_stats = knowledge_base.get_stats()
        token_info = response_generator.get_token_estimate()
        
        duration = datetime.now() - session_stats['start_time']
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return jsonify({
            'session': {
                'total_queries': session_stats['total_queries'],
                'duration': f"{hours}h {minutes}m {seconds}s",
                'conversation_turns': token_info['turns']
            },
            'knowledge_base': {
                'total_documents': kb_stats['total_documents'],
                'categories': kb_stats.get('categories', {})
            },
            'model': {
                'name': config.OPENAI_MODEL,
                'embedding_model': config.OPENAI_EMBEDDING_MODEL
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve audio files."""
    try:
        audio_path = Path(config.AUDIO_OUTPUT_PATH) / filename
        if audio_path.exists():
            return send_file(audio_path, mimetype='audio/wav')
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history."""
    try:
        history = response_generator.get_conversation_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌐 CHATBOT WEB APPLICATION")
    print("="*70)
    print(f"\n✅ Server starting...")
    print(f"📊 Knowledge Base: {knowledge_base.collection.count()} documents loaded")
    print(f"🤖 Model: {config.OPENAI_MODEL}")
    print(f"🔊 TTS: {'Enabled' if tts_service.model else 'Disabled'}")
    print(f"\n🌐 Access the chatbot at: http://localhost:5001")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
