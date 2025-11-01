# AI Chatbot System with Web Interface

A complete AI chatbot system with modern web interface that combines vector database storage, natural language generation, and text-to-speech capabilities.

## Features

- 🌐 **Modern Web Interface**: Beautiful browser-based UI with dark theme
- 🗄️ **ChromaDB Vector Database**: Store and retrieve knowledge using embeddings
- 🤖 **OpenAI SDK**: Generate intelligent natural language responses
- 🔊 **HuggingFace TTS**: Convert text responses to speech using VITS model
- 💬 **Multi-turn Conversations**: Maintain conversation context and history
- � **Statistics Dashboard**: Track queries, responses, and performance
- 📱 **Mobile Responsive**: Works on all devices

## Project Structure

```
AI_Chatbot_System/
├── web_app.py              # Flask web application (PRIMARY)
├── run_chatbot.py          # CLI entry point
├── templates/
│   └── index.html          # Web UI template
├── static/
│   ├── style.css           # Modern dark theme styling
│   └── script.js           # Frontend interactivity
├── src/
│   ├── chatbot.py          # Core chatbot logic
│   ├── knowledge_base.py   # ChromaDB integration
│   ├── response_generator.py # OpenAI integration
│   ├── tts_service.py      # Text-to-speech service
│   └── config.py           # Configuration settings
├── data/
│   └── faqs.json           # Mock FAQ data
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Example environment configuration
├── chroma_db/              # ChromaDB storage (auto-created)
├── audio_responses/        # Generated audio files (auto-created)
└── conversation_logs/      # Conversation history (auto-created)
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run the Chatbot

**Web Interface (Recommended)**:
```bash
python web_app.py
# Open browser to: http://localhost:5001
```

**Command Line Interface**:
```bash
python run_chatbot.py
```

## Usage

The chatbot provides an interactive CLI interface where you can:
- Ask questions that will be answered using the knowledge base
- Have responses converted to speech automatically
- Maintain multi-turn conversations with context
- Type 'quit' or 'exit' to end the conversation

## Components

### ChromaDB Integration
- Stores FAQs and knowledge base entries as embeddings
- Performs similarity search to find relevant context
- Automatically retrieves top-k relevant documents

### OpenAI SDK
- Generates contextual responses based on retrieved knowledge
- Maintains conversation history for multi-turn interactions
- Uses GPT models for high-quality responses

### HuggingFace TTS
- Converts text responses to natural-sounding speech
- Uses VITS model for high-quality audio generation
- Saves audio files for playback

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for first-time model downloads)
- Sufficient disk space for TTS models (~1-2GB)

## License

Educational project for AI workshop demonstration.
