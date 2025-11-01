# Chatbot System - Complete Guide

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Internet connection (for first-time model downloads)
- ~2GB disk space for TTS models

### Installation

1. **Clone or navigate to the project**
   ```bash
   cd Workshop_03
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   This will:
   - Check Python version
   - Create `.env` file from template
   - Install all dependencies
   - Optionally run component tests

3. **Configure your API key**
   ```bash
   # Edit .env file and add your OpenAI API key
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. **Run the chatbot**
   ```bash
   python chatbot.py
   ```

## 📁 Project Structure

```
Workshop_03/
├── chatbot.py              # Main chatbot application (CLI interface)
├── knowledge_base.py       # ChromaDB integration for vector storage
├── response_generator.py   # OpenAI SDK for response generation
├── tts_service.py          # HuggingFace TTS for audio generation
├── config.py               # Configuration management
├── setup.py                # Setup and installation script
├── examples.py             # Usage examples and demonstrations
├── test_chatbot.py         # Unit tests
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (you create this)
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore rules
├── README.md              # Project overview
├── GUIDE.md               # This comprehensive guide
├── data/
│   └── faqs.json          # Sample FAQ knowledge base
├── chroma_db/             # ChromaDB storage (auto-created)
├── audio_responses/       # Generated audio files (auto-created)
└── conversation_logs/     # Conversation history (auto-created)
```

## 🔧 Component Details

### 1. Knowledge Base (`knowledge_base.py`)

**Purpose**: Store and retrieve information using ChromaDB vector database

**Key Features**:
- Vector-based semantic search
- OpenAI embeddings for better accuracy
- Persistent storage
- Easy data management

**Usage**:
```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()
kb.load_faqs_from_json()  # Load from data/faqs.json

# Search for relevant information
results = kb.search("How do I reset my password?", top_k=3)
print(f"Found {results['count']} relevant documents")
```

### 2. Response Generator (`response_generator.py`)

**Purpose**: Generate natural language responses using OpenAI

**Key Features**:
- Context-aware responses
- Conversation history management
- Multi-turn dialogue support
- Token usage estimation

**Usage**:
```python
from response_generator import ResponseGenerator

rg = ResponseGenerator()

# Generate response with context
response = rg.generate_response(
    user_query="What are your hours?",
    context=context_from_kb,
    include_history=True
)
print(response)

# Save conversation
rg.save_conversation_log("my_conversation.txt")
```

### 3. TTS Service (`tts_service.py`)

**Purpose**: Convert text responses to natural speech

**Key Features**:
- HuggingFace VITS model
- High-quality audio generation
- Batch processing support
- Auto-normalization

**Usage**:
```python
from tts_service import TTSService

tts = TTSService()

# Convert single text
audio_path = tts.text_to_speech(
    "Hello! How can I help you?",
    output_filename="greeting.wav"
)

# Batch convert
texts = ["Response 1", "Response 2", "Response 3"]
audio_files = tts.batch_convert(texts, prefix="batch")
```

### 4. Main Chatbot (`chatbot.py`)

**Purpose**: Integrate all components into a complete system

**Key Features**:
- Interactive CLI interface
- Full query pipeline
- Session management
- Conversation logging

**Usage**:
```bash
# Standard mode
python chatbot.py

# Without TTS (faster, text-only)
python chatbot.py --no-tts

# Without knowledge base initialization
python chatbot.py --no-kb
```

## 💬 Interactive Commands

When running the chatbot, you can use these commands:

| Command | Description |
|---------|-------------|
| `quit` or `exit` | End the conversation |
| `history` | View full conversation history |
| `clear` | Clear conversation history |
| `stats` | Show chatbot statistics |
| `save` | Save conversation to file |
| `help` | Show available commands |

## 📚 Usage Examples

Run the examples script to see demonstrations:

```bash
python examples.py
```

Available examples:
1. Knowledge base search
2. Response generation
3. Multi-turn conversation
4. Text-to-speech conversion
5. Full pipeline demonstration
6. Batch operations
7. Custom knowledge addition

## 🧪 Testing

### Run all tests:
```bash
python test_chatbot.py
```

### Test individual components:
```bash
# Test knowledge base
python knowledge_base.py

# Test response generator
python response_generator.py

# Test TTS service
python tts_service.py
```

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional - customize these
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
CHROMA_DB_PATH=./chroma_db
AUDIO_OUTPUT_PATH=./audio_responses
```

### Configuration Options (`config.py`)

```python
# OpenAI settings
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4"
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"

# ChromaDB settings
COLLECTION_NAME = "knowledge_base"
TOP_K_RESULTS = 3  # Number of relevant docs to retrieve

# Conversation settings
MAX_HISTORY_TURNS = 10  # Maximum conversation turns to keep

# TTS settings
TTS_MODEL_NAME = "facebook/mms-tts-eng"
```

## 🎯 Common Use Cases

### 1. Customer Service Bot
```python
chatbot = Chatbot(enable_tts=True)
chatbot.initialize_knowledge_base()
chatbot.run_interactive()
```

### 2. FAQ Automation
```python
kb = KnowledgeBase()
kb.load_faqs_from_json("data/faqs.json")

for question in user_questions:
    results = kb.search(question)
    print(kb.format_context(results))
```

### 3. Voice-enabled Assistant
```python
tts = TTSService()
rg = ResponseGenerator()

response = rg.generate_response(user_query)
audio = tts.text_to_speech(response, play_audio=True)
```

## 🔍 Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: Edit `.env` file and add your OpenAI API key

### Issue: TTS model download fails
**Solution**: 
- Check internet connection
- Ensure sufficient disk space (~2GB)
- Try manually: `python tts_service.py`

### Issue: ChromaDB errors
**Solution**: 
- Delete `chroma_db/` folder
- Run `python knowledge_base.py` to reinitialize

### Issue: Import errors
**Solution**: 
```bash
pip install -r requirements.txt --upgrade
```

## 📊 Performance Tips

1. **Use GPT-3.5-turbo for faster responses**
   - Set `OPENAI_MODEL=gpt-3.5-turbo` in `.env`

2. **Disable TTS for text-only mode**
   ```bash
   python chatbot.py --no-tts
   ```

3. **Limit conversation history**
   - Adjust `MAX_HISTORY_TURNS` in `config.py`

4. **Reduce knowledge base search**
   - Adjust `TOP_K_RESULTS` in `config.py`

## 🔐 Security Best Practices

1. **Never commit `.env` file**
   - It's in `.gitignore` by default

2. **Rotate API keys regularly**
   - Update in `.env` file

3. **Use environment-specific configs**
   - Development vs. production `.env` files

4. **Monitor API usage**
   - Check OpenAI dashboard regularly

## 📈 Extending the System

### Add New Knowledge Sources

```python
# Load from custom JSON
kb.load_faqs_from_json("custom_data.json")

# Add individual documents
kb.add_document(
    document="Custom content here",
    metadata={"category": "custom", "source": "manual"},
    doc_id="custom_001"
)
```

### Customize System Prompt

```python
rg = ResponseGenerator()
rg.set_system_prompt("""
Your custom system prompt here.
Define the bot's personality and behavior.
""")
```

### Add New TTS Languages

```python
# Use multilingual model
tts = TTSService(model_name="facebook/mms-tts-fra")  # French
```

## 📝 Best Practices

1. **Initialize once, use multiple times**
   ```python
   chatbot = Chatbot()  # Initialize once
   for query in queries:
       chatbot.process_query(query)  # Reuse
   ```

2. **Save conversations regularly**
   ```python
   chatbot.response_generator.save_conversation_log()
   ```

3. **Clean up old files**
   ```python
   tts.cleanup_old_files(days=7)
   ```

4. **Monitor token usage**
   ```python
   tokens = rg.get_token_estimate()
   print(f"Estimated tokens: {tokens['total_estimate']}")
   ```

## 🎓 Learning Path

1. **Start with examples**: `python examples.py`
2. **Test individual components**: Run each `.py` file directly
3. **Run interactive chatbot**: `python chatbot.py`
4. **Customize knowledge base**: Edit `data/faqs.json`
5. **Modify system behavior**: Edit `config.py`
6. **Build your own application**: Use components as building blocks

## 📞 Support

- Check examples: `python examples.py`
- Run tests: `python test_chatbot.py`
- Review logs in `conversation_logs/`
- Check OpenAI API status: https://status.openai.com/

## 📄 License

Educational project for workshop demonstration purposes.

---

**Built with**: ChromaDB, OpenAI SDK, HuggingFace Transformers
**Last Updated**: November 2025
