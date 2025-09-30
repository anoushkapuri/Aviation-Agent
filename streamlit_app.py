import streamlit as st
import os
import hashlib
import time
import json
from agent import AviationAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Aviation Intelligence Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional dark theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables */
    :root {
        --primary-color: #0066cc;
        --secondary-color: #004499;
        --accent-color: #ff6b35;
        --bg-primary: #ffffff;
        --bg-secondary: #f5f5f5;
        --bg-tertiary: #ffffff;
        --text-primary: #212529;
        --text-secondary: #6c757d;
        --text-muted: #868e96;
        --border-color: #dee2e6;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --error-color: #dc3545;
    }
    
    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background: transparent;
        color: var(--text-primary);
    }
    
    /* Streamlit branding visible */
    
    /* Make Streamlit rerun text visible */
    .stAlert, .stException, .stMarkdown, .stText, .stCode, .stDataFrame, 
    .stSelectbox, .stTextInput, .stTextArea, .stNumberInput, .stSlider, 
    .stCheckbox, .stRadio, .stButton, .stFileUploader, .stDownloadButton,
    .stProgress, .stSpinner, .stBalloons, .stSnow, .stSuccess, .stInfo, 
    .stWarning, .stError, .stSidebar, .stExpander, .stContainer, 
    .stColumns, .stTabs, .stChatInput, .stChatMessage {
        color: var(--text-primary) !important;
    }
    
    /* Streamlit rerun and error messages */
    .stAlert > div, .stException > div, .stMarkdown > div, 
    .stText > div, .stCode > div, .stDataFrame > div {
        color: var(--text-primary) !important;
        background: transparent !important;
    }
    
    /* Make all text elements white */
    p, span, div, label, input, textarea, select, button {
        color: var(--text-primary) !important;
    }
    
    /* Specific Streamlit elements */
    .stTextInput label, .stTextArea label, .stSelectbox label, 
    .stNumberInput label, .stSlider label, .stCheckbox label, 
    .stRadio label, .stFileUploader label {
        color: var(--text-primary) !important;
    }
    
    /* Custom header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        background: transparent !important;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        background: transparent !important;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    
    .status-success {
        background: rgba(40, 167, 69, 0.1);
        color: var(--success-color);
        border: 1px solid rgba(40, 167, 69, 0.2);
    }
    
    .status-warning {
        background: rgba(255, 193, 7, 0.1);
        color: var(--warning-color);
        border: 1px solid rgba(255, 193, 7, 0.2);
    }
    
    .status-error {
        background: rgba(220, 53, 69, 0.1);
        color: var(--error-color);
        border: 1px solid rgba(220, 53, 69, 0.2);
    }
    
    /* Chat container */
    .chat-container {
        background: transparent;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }
    
    /* Chat bubbles with smooth animations */
    .user-bubble {
        background: #ff0000 !important;
        color: white !important;
        padding: 1rem 1.25rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.75rem 0;
        text-align: right;
        width: fit-content;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.2);
        animation: slideInRight 0.3s ease-out;
        font-weight: 500;
        line-height: 1.5;
    }
    
    .assistant-bubble {
        background: #6c757d !important;
        color: white !important;
        padding: 1rem 1.25rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.75rem 0;
        text-align: left;
        max-width: 85%;
        margin-right: auto;
        border: 1px solid #5a6268;
        box-shadow: 0 4px 12px rgba(108, 117, 125, 0.2);
        animation: slideInLeft 0.3s ease-out;
        line-height: 1.6;
    }
    
    /* Ensure all text inside chat bubbles is white */
    .user-bubble *, .assistant-bubble * {
        color: white !important;
    }
    
    .user-bubble p, .assistant-bubble p {
        color: white !important;
    }
    
    .user-bubble span, .assistant-bubble span {
        color: white !important;
    }
    
    .user-bubble div, .assistant-bubble div {
        color: white !important;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid var(--border-color);
        border-radius: 50%;
        border-top-color: var(--primary-color);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Source documents expander */
    .source-docs {
        background: var(--bg-tertiary);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    .source-doc-item {
        background: transparent;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid var(--primary-color);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        min-height: 2.5rem;
        resize: vertical;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2);
        outline: none;
    }
    
    /* Chat input container styling */
    .stChatInput > div {
        background: transparent !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        border: 1px solid var(--border-color) !important;
        backdrop-filter: blur(10px) !important;
        color: var(--text-primary) !important;
    }
    
    .stChatInput > div > div > div > div > input {
        background: white !important;
        border: 1px solid #dee2e6 !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        min-height: 2.5rem !important;
        resize: vertical !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stChatInput > div > div > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2) !important;
        outline: none !important;
        background: white !important;
        color: var(--text-primary) !important;
    }
    
    .stChatInput > div > div > div > div > input::placeholder {
        color: var(--text-muted) !important;
        font-style: italic !important;
        opacity: 0.7 !important;
    }
    
    /* Ensure all chat input text is visible */
    .stChatInput, .stChatInput *, .stChatInput input, .stChatInput textarea {
        color: var(--text-primary) !important;
        background-color: white !important;
    }
    
    /* Chat input label styling */
    .stChatInput label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    /* Send button styling */
    .stChatInput > div > div > div > div > button {
        background: var(--primary-color) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        margin-left: 0.5rem !important;
    }
    
    .stChatInput > div > div > div > div > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.3) !important;
    }
    
    /* Enhanced input flexibility */
    .stChatInput > div > div > div > div {
        display: flex !important;
        align-items: flex-end !important;
        gap: 0.5rem !important;
    }
    
    .stChatInput > div > div > div > div > input {
        flex: 1 !important;
        min-height: 2.5rem !important;
        max-height: 8rem !important;
        overflow-y: auto !important;
        word-wrap: break-word !important;
        white-space: pre-wrap !important;
        line-height: 1.5 !important;
    }
    
    /* Auto-resize textarea behavior */
    .stChatInput > div > div > div > div > input[type="text"] {
        height: auto !important;
        min-height: 2.5rem !important;
    }
    
    /* Focus states and animations */
    .stChatInput > div > div > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2) !important;
        outline: none !important;
        transform: scale(1.01) !important;
    }
    
    /* Input container hover effect */
    .stChatInput > div:hover {
        border-color: rgba(0, 102, 204, 0.3) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Comprehensive Streamlit white theme */
    .stApp > div {
        background: transparent !important;
        color: var(--text-primary) !important;
    }
    
    /* All Streamlit widgets white theme */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stSlider > div > div > input,
    .stCheckbox > div > div > input,
    .stRadio > div > div > input,
    .stFileUploader > div > div > input {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Streamlit status messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        background: transparent !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stSuccess {
        border-left: 4px solid var(--success-color) !important;
    }
    
    .stInfo {
        border-left: 4px solid var(--primary-color) !important;
    }
    
    .stWarning {
        border-left: 4px solid var(--warning-color) !important;
    }
    
    .stError {
        border-left: 4px solid var(--error-color) !important;
    }
    
    /* Streamlit spinner and progress */
    .stSpinner, .stProgress {
        color: var(--primary-color) !important;
    }
    
    /* Streamlit expander */
    .stExpander > div {
        background: transparent !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stExpander > div > div {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Streamlit columns and containers */
    .stColumns > div, .stContainer > div {
        background: transparent !important;
        color: var(--text-primary) !important;
    }
    
    /* Streamlit tabs */
    .stTabs > div {
        background: transparent !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .stTabs > div > div {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Streamlit sidebar */
    .stSidebar > div {
        background: transparent !important;
        border-right: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Streamlit dataframe */
    .stDataFrame {
        background: transparent !important;
        color: var(--text-primary) !important;
    }
    
    /* Streamlit code blocks */
    .stCode {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Override any remaining white backgrounds */
    div[data-testid="stApp"] {
        background: transparent !important;
    }
    
    div[data-testid="stApp"] > div {
        background: transparent !important;
        color: var(--text-primary) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.3);
    }
    
    /* Metrics and info boxes */
    .metric-card {
        background: transparent;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .user-bubble, .assistant-bubble {
            max-width: 90%;
        }
    }
    
    /* Smooth transitions */
    * {
        transition: all 0.2s ease;
    }
    </style>
    
    <script>
    // Auto-resize input functionality
    function autoResizeInput() {
        const inputs = document.querySelectorAll('.stChatInput input[type="text"]');
        inputs.forEach(input => {
            // Set initial height
            input.style.height = 'auto';
            input.style.height = Math.max(input.scrollHeight, 40) + 'px';
            
            // Add event listener for input changes
            input.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.max(this.scrollHeight, 40) + 'px';
            });
            
            // Handle paste events
            input.addEventListener('paste', function() {
                setTimeout(() => {
                    this.style.height = 'auto';
                    this.style.height = Math.max(this.scrollHeight, 40) + 'px';
                }, 0);
            });
        });
    }
    
    // Run on page load and when new content is added
    document.addEventListener('DOMContentLoaded', autoResizeInput);
    
    // Use MutationObserver to detect when Streamlit adds new elements
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                autoResizeInput();
            }
        });
    });
    
    // Start observing
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    </script>
""", unsafe_allow_html=True)

# Chat history storage functions
def save_chat_history(chat_history):
    """Save chat history to a local file."""
    try:
        with open('chat_history.json', 'w') as f:
            json.dump(chat_history, f)
    except Exception as e:
        st.error(f"Error saving chat history: {str(e)}")

def load_chat_history():
    """Load chat history from local file."""
    try:
        if os.path.exists('chat_history.json'):
            with open('chat_history.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading chat history: {str(e)}")
    return []

def clear_chat_history():
    """Clear chat history from both session state and file."""
    st.session_state.chat_history = []
    try:
        if os.path.exists('chat_history.json'):
            os.remove('chat_history.json')
    except Exception as e:
        st.error(f"Error clearing chat history: {str(e)}")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()  # Load from file
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False
if "auto_load_attempted" not in st.session_state:
    st.session_state.auto_load_attempted = False

@st.cache_resource
def initialize_agent():
    """Initialize the agent with OpenAI API key from environment variables. Cached to persist across sessions."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return AviationAgent(api_key)

@st.cache_data
def get_pdf_files_hash():
    """Get hash of PDF files to detect changes."""
    pdf_dir = "test_pdfs"
    if not os.path.exists(pdf_dir):
        return "no_pdfs"
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    pdf_files.sort()
    
    combined_hash = ""
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        if os.path.exists(pdf_path):
            stat = os.stat(pdf_path)
            # Include file path, size, and modification time in hash
            hash_string = f"{pdf_path}_{stat.st_size}_{stat.st_mtime}"
            combined_hash += hashlib.md5(hash_string.encode()).hexdigest()
    
    return hashlib.md5(combined_hash.encode()).hexdigest()

@st.cache_resource
def load_documents_cached(_agent, pdf_hash):
    """Load and process documents with Streamlit caching. Uses pdf_hash to invalidate cache when files change."""
    success = _agent.load_documents(directory_path=None)
    if success:
        return True
    else:
        st.error("❌ Failed to load documents")
        return False

def auto_load_documents():
    """Automatically load documents using cached processing."""
    if st.session_state.agent is None:
        return False
    
    try:
        # Get current PDF files hash
        pdf_hash = get_pdf_files_hash()
        
        # Use cached document loading
        success = load_documents_cached(st.session_state.agent, pdf_hash)
        if success:
            st.session_state.documents_loaded = True
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error auto-loading documents: {str(e)}")
        return False

def main():
    # Professional header with gradient text
    st.markdown('<div class="main-header">Arup Aviation Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced Document Analysis for Aviation Planning Teams</div>', unsafe_allow_html=True)

    # Initialize agent if not already done
    if st.session_state.agent is None:
        try:
            st.session_state.agent = initialize_agent()
        except ValueError as e:
            st.markdown(f'<div class="status-indicator status-error">❌ {str(e)}</div>', unsafe_allow_html=True)
            return

    # Auto-load documents from default directory if not already attempted
    if not st.session_state.auto_load_attempted and not st.session_state.documents_loaded:
        with st.spinner("🔄 Loading documents..."):
            if not auto_load_documents():
                st.markdown('<div class="status-indicator status-error">❌ Failed to load documents. Please check your setup.</div>', unsafe_allow_html=True)
        st.session_state.auto_load_attempted = True

    # System status (simplified)
    # Removed system ready message

    # Chat interface
    # Add clear chat button if there's chat history
    if st.session_state.chat_history:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 💬 Intelligent Document Assistant", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️ Clear Chat", help="Clear conversation history"):
                clear_chat_history()
                st.rerun()
    else:
        st.markdown("### 💬 Intelligent Document Assistant", unsafe_allow_html=True)
    
    st.markdown("Ask questions about aviation planning, regulations, and design standards.")
    
    # Display chat history with smooth animations
    if st.session_state.chat_history:
        st.markdown("---")
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-bubble">{message["content"]}</div>', unsafe_allow_html=True)

    # Enhanced chat input
    if prompt := st.chat_input("Ask about aviation planning, regulations, or design standards..."):
        if not st.session_state.documents_loaded:
            st.markdown('<div class="status-indicator status-warning">⚠️ Please wait for documents to load or check your setup!</div>', unsafe_allow_html=True)
            return

        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        save_chat_history(st.session_state.chat_history)  # Save to file
        
        # Display user message with animation
        st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)

        # Get agent response with enhanced loading
        with st.spinner("🔍 Analyzing aviation documents..."):
            try:
                response = st.session_state.agent.ask_question(prompt)
                
                # Add assistant message to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
                save_chat_history(st.session_state.chat_history)  # Save to file
                
                # Display assistant message with animation
                st.markdown(f'<div class="assistant-bubble">{response["answer"]}</div>', unsafe_allow_html=True)
                
                # Enhanced source documents display
                if response["source_documents"]:
                    with st.expander("📄 View Source Documents & Citations", expanded=False):
                        st.markdown('<div class="source-docs">', unsafe_allow_html=True)
                        for i, doc in enumerate(response["source_documents"], 1):
                            st.markdown(f"""
                            <div class="source-doc-item">
                                <strong>📋 Source Document {i}</strong><br>
                                <small style="color: var(--text-muted);">Relevance Score: {getattr(doc, 'score', 'N/A')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(doc.page_content)
                            st.markdown("---")
                        st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="status-indicator status-error">❌ Error processing request: {str(e)}</div>', unsafe_allow_html=True)
    
    # Footer with simple branding - moved below chat input
    st.markdown("""
    <div style="text-align: center; color: var(--text-muted); font-size: 0.9rem; margin-top: 1rem;">
        <p>Built for Arup by Anoushka Puri. Please double-check AI responses.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()