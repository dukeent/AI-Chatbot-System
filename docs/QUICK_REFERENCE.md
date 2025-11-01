# CHATBOT SYSTEM - QUICK REFERENCE CARD

## ⚡ Quick Commands

### First Time Setup
```bash
python setup.py              # Run automated setup
# Edit .env - add OPENAI_API_KEY
python demo.py               # Try offline demo
python chatbot.py            # Run full chatbot
```

### Running the Chatbot
```bash
python chatbot.py            # Standard mode (with TTS)
python chatbot.py --no-tts   # Text-only (faster)
python chatbot.py --no-kb    # Skip KB initialization
```

### Testing & Demos
```bash
python demo.py               # Offline demo (no API key needed)
python examples.py           # 7 usage examples
python test_chatbot.py       # Run unit tests
python knowledge_base.py     # Test ChromaDB
python response_generator.py # Test OpenAI
python tts_service.py        # Test TTS
```

---

## 💬 Interactive Commands (in chatbot)

| Command | Action |
|---------|--------|
| `quit` / `exit` | End conversation |
| `history` | View conversation history |
| `clear` | Clear conversation history |
| `stats` | Show chatbot statistics |
| `save` | Save conversation log |
| `help` | Show commands |

---

## 📁 File Quick Reference

| File | Purpose | When to Edit |
|------|---------|--------------|
| `chatbot.py` | Main app | Customize UI, commands |
| `knowledge_base.py` | ChromaDB | Modify search logic |
| `response_generator.py` | OpenAI | Change prompts, behavior |
| `tts_service.py` | TTS | Adjust audio settings |
| `config.py` | Settings | Change defaults |
| `.env` | API keys | Add your keys |
| `data/faqs.json` | Knowledge | Add/edit FAQs |

---

## 🔧 Configuration Quick Edit

### .env File
```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo        # or gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
CHROMA_DB_PATH=./chroma_db
AUDIO_OUTPUT_PATH=./audio_responses
```

### config.py Settings
```python
MAX_HISTORY_TURNS = 10    # Conversation turns to keep
TOP_K_RESULTS = 3         # Documents to retrieve
TTS_MODEL_NAME = "facebook/mms-tts-eng"  # TTS model
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "OPENAI_API_KEY not found" | Add key to `.env` file |
| Import errors | Run `pip install -r requirements.txt` |
| TTS download fails | Check internet, disk space |
| ChromaDB errors | Delete `chroma_db/` folder |
| Slow responses | Use `--no-tts` flag |

---

## 📚 Documentation Files

| File | Content |
|------|---------|
| `README.md` | Project overview, quick start |
| `GUIDE.md` | Comprehensive usage guide |
| `DELIVERABLES.md` | Workshop requirements checklist |
| `PROJECT_SUMMARY.md` | Complete project summary |
| `ARCHITECTURE.md` | System diagrams |
| `QUICK_REFERENCE.md` | This file |

---

## 🎯 Common Tasks

### Add New FAQs
1. Edit `data/faqs.json`
2. Add entry with: id, question, answer, category
3. Run chatbot (will auto-load)

### Change Bot Personality
1. Edit `response_generator.py`
2. Modify `self.system_prompt`
3. Restart chatbot

### Use Different TTS Voice
1. Edit `config.py`
2. Change `TTS_MODEL_NAME`
3. Find models at: huggingface.co/models?pipeline_tag=text-to-speech

### Export Conversation
- In chatbot: type `save`
- Or: `response_generator.save_conversation_log()`
- Files in: `conversation_logs/`

---

## 🔑 Key Concepts

### RAG (Retrieval Augmented Generation)
```
Query → Search DB → Get Context → LLM → Response
```

### Vector Embeddings
```
Text → Embeddings → Vector → Similarity Search
```

### Multi-turn Conversation
```
History[Turn1, Turn2, ...] + NewQuery → Context-aware Response
```

---

## 📊 Component Functions

### KnowledgeBase (ChromaDB)
```python
kb = KnowledgeBase()
kb.load_faqs_from_json()
results = kb.search("query", top_k=3)
context = kb.format_context(results)
```

### ResponseGenerator (OpenAI)
```python
rg = ResponseGenerator()
response = rg.generate_response(query, context)
rg.save_conversation_log("file.txt")
```

### TTSService (HuggingFace)
```python
tts = TTSService()
audio = tts.text_to_speech("text", "file.wav")
tts.batch_convert(texts, "prefix")
```

---

## ⚙️ Dependencies Quick List

```
openai          # OpenAI API
chromadb        # Vector database
transformers    # HuggingFace models
torch           # PyTorch for TTS
soundfile       # Audio I/O
colorama        # Colored CLI
python-dotenv   # Environment vars
```

---

## 🚀 Performance Tips

1. **Fast Mode**: Use `--no-tts` flag
2. **Reduce History**: Lower `MAX_HISTORY_TURNS`
3. **Fewer Results**: Lower `TOP_K_RESULTS`
4. **Use GPT-3.5**: Faster than GPT-4
5. **Cache Models**: Models download once, then cached

---

## 📈 Typical Response Times

| Operation | Time |
|-----------|------|
| KB Search | <1s |
| OpenAI Call | 2-5s |
| TTS Generation | 3-8s |
| Total Pipeline | 5-15s |

---

## 🎓 Learning Path

1. ✅ Run `demo.py` (offline)
2. ✅ Run `examples.py` (learn patterns)
3. ✅ Try `chatbot.py` (full experience)
4. ✅ Read `GUIDE.md` (deep dive)
5. ✅ Modify `faqs.json` (customize)
6. ✅ Extend system (build features)

---

## 🔗 Useful Links

- OpenAI Docs: https://platform.openai.com/docs
- ChromaDB Docs: https://docs.trychroma.com
- HuggingFace Models: https://huggingface.co/models
- VITS Paper: https://arxiv.org/abs/2106.06103

---

## 💡 Pro Tips

1. **Start Simple**: Try demo mode first
2. **Read Logs**: Check conversation_logs/ for debugging
3. **Test Components**: Run individual .py files
4. **Use Examples**: examples.py shows best practices
5. **Monitor Usage**: Check OpenAI dashboard for API costs
6. **Save Often**: Use `save` command in chatbot
7. **Clean Audio**: Use `tts.cleanup_old_files()`

---

## 📞 Getting Help

1. **Check Examples**: `python examples.py`
2. **Read Docs**: See GUIDE.md
3. **Run Tests**: `python test_chatbot.py`
4. **Check Logs**: Look in conversation_logs/
5. **Try Demo**: `python demo.py` works offline

---

**🎉 You're Ready to Go!**

```bash
# Quick start (no API needed)
python demo.py

# Full chatbot (requires API key)
python chatbot.py
```

**Last Updated**: November 1, 2025
