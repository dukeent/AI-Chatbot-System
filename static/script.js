// Global state
let isAudioEnabled = true;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    autoResizeTextarea();
    loadStats();
});

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Auto-resize textarea
function autoResizeTextarea() {
    const textarea = document.getElementById('messageInput');
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
}

// Send message
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    input.value = '';
    input.style.height = 'auto';
    
    // Show loading
    showLoading(true);
    
    // Get audio toggle state
    const audioToggle = document.getElementById('audioToggle');
    isAudioEnabled = audioToggle.checked;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                enable_audio: isAudioEnabled
            })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Add bot response to chat
        addMessage(data.response, 'bot', data.audio_url, data.sources_found, data.timestamp);
        
        // Update stats
        loadStats();
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
        showLoading(false);
    }
}

// Add message to chat
function addMessage(text, sender, audioUrl = null, sourcesFound = 0, timestamp = null) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.innerHTML = formatMessage(text);
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = timestamp || getTimeString();
    
    contentDiv.appendChild(textDiv);
    
    // Add sources indicator for bot messages
    if (sender === 'bot' && sourcesFound > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'message-sources';
        sourcesDiv.innerHTML = `📚 ${sourcesFound} knowledge base ${sourcesFound === 1 ? 'source' : 'sources'} used`;
        contentDiv.appendChild(sourcesDiv);
    }
    
    // Add audio player if available
    if (audioUrl) {
        const audioDiv = document.createElement('div');
        audioDiv.className = 'audio-player';
        audioDiv.innerHTML = `
            <audio controls>
                <source src="${audioUrl}" type="audio/wav">
                Your browser does not support the audio element.
            </audio>
        `;
        contentDiv.appendChild(audioDiv);
    }
    
    contentDiv.appendChild(timeDiv);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format message text (convert markdown-like syntax)
function formatMessage(text) {
    // Convert newlines to <br>
    text = text.replace(/\n/g, '<br>');
    
    // Convert **bold** to <strong>
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
    
    return text;
}

// Get current time string
function getTimeString() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Show/hide loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}

// Toggle stats panel
function toggleStats() {
    const statsPanel = document.getElementById('statsPanel');
    statsPanel.classList.toggle('hidden');
    
    if (!statsPanel.classList.contains('hidden')) {
        loadStats();
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        document.getElementById('statQueries').textContent = data.session.total_queries;
        document.getElementById('statDuration').textContent = data.session.duration;
        document.getElementById('statTurns').textContent = data.session.conversation_turns;
        document.getElementById('statDocs').textContent = data.knowledge_base.total_documents;
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Clear chat
async function clearChat() {
    if (!confirm('Are you sure you want to clear the conversation history?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/clear', {
            method: 'POST'
        });
        
        if (response.ok) {
            // Clear chat messages except the welcome message
            const chatMessages = document.getElementById('chatMessages');
            const welcomeMessage = chatMessages.firstElementChild;
            chatMessages.innerHTML = '';
            chatMessages.appendChild(welcomeMessage);
            
            // Update stats
            loadStats();
            
            // Show notification
            addMessage('Conversation history has been cleared.', 'bot');
        }
    } catch (error) {
        console.error('Error clearing chat:', error);
        alert('Failed to clear chat history.');
    }
}

// Handle audio toggle
document.getElementById('audioToggle').addEventListener('change', (e) => {
    isAudioEnabled = e.target.checked;
    console.log('Audio', isAudioEnabled ? 'enabled' : 'disabled');
});
