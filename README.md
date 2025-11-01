# 🤖 AI Chatbot System with Web Interface

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete, production-ready chatbot system with **modern web interface**, combining vector database storage, natural language generation, and text-to-speech capabilities.

## ✨ Features

- 🌐 **Modern Web Interface** - Beautiful, responsive chat UI
- 🗄️ **ChromaDB Vector Database** - Intelligent knowledge storage and retrieval
- 🤖 **OpenAI SDK** - GPT-powered natural language responses  
- 🔊 **HuggingFace TTS** - High-quality voice output with in-browser playback
- 💬 **Multi-turn Conversations** - Context-aware dialogue with history
- � **Real-time Statistics** - Track queries, duration, and performance
- 🎨 **Dark Theme UI** - Modern, professional design
- 📱 **Mobile Responsive** - Works on all devices

## 🚀 Quick Start

### Option 1: Web Interface (Recommended!)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your API key
cp .env.example .env
# Edit .env and add your OpenAI API key

# 3. Start the web server
python web_app.py

# 4. Open your browser
# Visit: http://localhost:5000
```

### Option 2: Command-Line Interface
```bash
python run_chatbot.py
```

### Option 3: Try the Demo (No Setup!)
```bash
python utils/demo.py
```
**No API key needed** - See the system in action immediately!

## 📁 Project Structure

```
Workshop_03/
├── web_app.py                # Flask web application (NEW!)
├── run_chatbot.py            # CLI entry point
│
├── templates/                 # Web interface (NEW!)
│   └── index.html            # Chat UI
│
├── static/                    # Frontend assets (NEW!)
│   ├── style.css             # Modern dark theme
│   └── script.js             # Interactive features
│
├── src/                       # Core application code
│   ├── chatbot.py            # Main chatbot logic
│   ├── knowledge_base.py     # ChromaDB integration
│   ├── response_generator.py # OpenAI integration
│   ├── tts_service.py        # Text-to-Speech service
│   └── config.py             # Configuration management
│
├── utils/                     # Utility scripts
│   ├── setup.py              # Automated setup wizard
│   ├── demo.py               # Offline demonstration
│   └── examples.py           # Usage examples (7 demos)
│
├── tests/                     # Test suite
│   └── test_chatbot.py       # Unit tests
│
├── docs/                      # Documentation
│   ├── START_HERE.md         # Beginner's guide
│   ├── GUIDE.md              # Comprehensive guide
│   └── ...more docs
│
├── data/                      # Knowledge base
│   └── faqs.json             # Sample FAQs (15 entries)
│
└── requirements.txt          # Dependencies
```

## 💬 Usage

### 🌐 Web Interface (Recommended)

1. **Start the server:**
```bash
python web_app.py
```

2. **Open your browser:**
```
http://localhost:5000
```

3. **Features:**
   - 💬 Real-time chat interface
   - 🔊 Toggle audio responses on/off
   - 📊 View session statistics
   - 🗑️ Clear conversation history
   - 📱 Works on mobile devices
   - 🎨 Beautiful dark theme

**Web Interface Controls:**
- Type your message and press Enter
- Click 🔊 Audio toggle to enable/disable TTS
- Click 📊 Stats to view session statistics
- Click 🗑️ Clear to reset conversation

### 🖥️ Command-Line Interface

**Interactive Mode:**
```bash
python run_chatbot.py
```

**Available Commands:**
- Ask any question
- `help` - Show commands
- `history` - View conversation
- `stats` - Show statistics
- `save` - Export conversation
- `quit` - Exit

### Options
```bash
python run_chatbot.py --no-tts    # Text-only (faster)
python run_chatbot.py --no-kb     # Skip knowledge base
```

### Try Examples
```bash
python utils/examples.py          # 7 usage demonstrations
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [START_HERE.md](docs/START_HERE.md) | **→ Start here!** Beginner's guide |
| [GUIDE.md](docs/GUIDE.md) | Comprehensive usage guide |
| [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) | Command cheat sheet |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture |
| [DELIVERABLES.md](docs/DELIVERABLES.md) | Workshop requirements |

## 🔧 Configuration

Edit `.env` file:
```bash
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-3.5-turbo
CHROMA_DB_PATH=./chroma_db
AUDIO_OUTPUT_PATH=./audio_responses
```

Edit `src/config.py` for advanced settings:
- `MAX_HISTORY_TURNS` - Conversation turns to keep
- `TOP_K_RESULTS` - Documents to retrieve
- `TTS_MODEL_NAME` - Text-to-speech model

## 🧪 Testing

```bash
# Run all tests
python tests/test_chatbot.py

# Test individual components
python src/knowledge_base.py
python src/response_generator.py
python src/tts_service.py
```

## 🎯 Use Cases

- **Customer Service Bot** - Answer FAQs automatically with web interface
- **Knowledge Base Assistant** - Search and retrieve information in real-time
- **Voice Assistant** - Text and voice responses with browser playback
- **Interactive Learning** - Educational chatbot with modern UI
- **Internal Support Tool** - Deploy as web service for team use
- **API Service** - REST endpoints for integration

## 🛠️ Built With

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [OpenAI API](https://platform.openai.com/) - Language models
- [HuggingFace Transformers](https://huggingface.co/) - TTS models
- [PyTorch](https://pytorch.org/) - ML framework
- HTML5, CSS3, JavaScript - Modern web interface

## 📊 Requirements

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ~2GB disk space (for TTS models)
- Internet connection (first-time model downloads)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| API key error | Add key to `.env` file |
| Import errors | Run `pip install -r requirements.txt` |
| Flask not installed | Run `pip install flask` |
| Port 5000 in use | Change port in `web_app.py` |
| TTS download fails | Check internet connection |
| Slow responses | Use `--no-tts` flag or disable audio in web UI |
| Browser can't connect | Check firewall, try `http://127.0.0.1:5000` |

See [GUIDE.md](docs/GUIDE.md) for detailed troubleshooting.

## 📈 Performance

**Web Interface:**
- Page load: <1s
- Message send: 5-15s (with TTS)
- Message send: 2-5s (without TTS)
- Audio playback: Instant (browser native)

**Backend:**
- Knowledge base search: <1s
- OpenAI response: 2-5s
- TTS generation: 3-8s
- Total pipeline: 5-15s per query

**Concurrent Users:** 
- Single server can handle 10-20 simultaneous users
- Use gunicorn/nginx for production scaling

## 🎓 Learning Resources

1. **Beginner**: Read [START_HERE.md](docs/START_HERE.md)
2. **Intermediate**: Try `python utils/examples.py`
3. **Advanced**: Study [ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 🤝 Contributing

This is an educational workshop project. Feel free to:
- Customize for your use case
- Add new features
- Improve documentation
- Share your implementations

## 📄 License

Educational project for workshop demonstration purposes.

## 🙏 Acknowledgments

- OpenAI for GPT models
- ChromaDB team for vector database
- HuggingFace for TTS models
- Workshop participants

---

## 🎉 Ready to Start?

### Web Interface (Recommended)
```bash
python web_app.py
# Then open: http://localhost:5000
```

### Command Line
```bash
python run_chatbot.py
```

### Quick Demo (No Setup)
```bash
python utils/demo.py
```

**Need help?** Read [START_HERE.md](docs/START_HERE.md) or [GUIDE.md](docs/GUIDE.md)

**Questions?** Check [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)

---

## 🌐 API Endpoints

The web application provides REST API endpoints:

- `GET /` - Chat interface
- `POST /api/chat` - Send message, get response
- `GET /api/stats` - Get session statistics
- `POST /api/clear` - Clear conversation history
- `GET /api/history` - Get conversation history
- `GET /audio/<filename>` - Serve audio files

Example API usage:
```javascript
fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        message: 'Hello!',
        enable_audio: true
    })
})
```

---

**Built with ❤️ for AI Workshop 2025**
