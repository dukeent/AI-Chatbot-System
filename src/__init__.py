"""
Chatbot System Package
Main components for the intelligent chatbot.
"""

__version__ = "1.0.0"
__author__ = "Workshop Team"

# Make imports easier
from src.config import *
from src.knowledge_base import KnowledgeBase
from src.response_generator import ResponseGenerator
from src.tts_service import TTSService
from src.chatbot import Chatbot

__all__ = [
    'KnowledgeBase',
    'ResponseGenerator',
    'TTSService',
    'Chatbot'
]
