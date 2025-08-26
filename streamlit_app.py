import streamlit as st
import os
import hashlib
import time
from agent import AviationAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Aviation Document Analysis",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
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
        st.success("✅ Documents processed and cached successfully!")
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
    st.title("✈️ Aviation Document Analysis")
    st.write("Ask questions about aviation planning documents!")

    # Initialize agent if not already done
    if st.session_state.agent is None:
        try:
            st.session_state.agent = initialize_agent()
        except ValueError as e:
            st.error(str(e))
            return

    # Auto-load documents from default directory if not already attempted
    if not st.session_state.auto_load_attempted and not st.session_state.documents_loaded:
        with st.spinner("Loading aviation documents..."):
            # Check if this is likely a cached load
            start_time = time.time()
            if auto_load_documents():
                load_time = time.time() - start_time
                if load_time < 2.0:
                    st.success("⚡ Documents loaded from cache! (No API costs)")
                else:
                    st.success("✅ Documents processed and cached for future use!")
                st.info("💡 Subsequent loads will be instant and cost-free!")
            else:
                st.error("❌ Failed to load documents. Please check your setup.")
        st.session_state.auto_load_attempted = True

    # Chat interface
    st.subheader("💬 Ask questions about the aviation documents")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the aviation documents"):
        if not st.session_state.documents_loaded:
            st.warning("Please wait for documents to load or check your setup!")
            return

        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get agent response
        with st.spinner("Analyzing documents..."):
            try:
                response = st.session_state.agent.ask_question(prompt)
                
                # Add assistant message to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
                
                # Display assistant message
                with st.chat_message("assistant"):
                    st.write(response["answer"])
                    
                    # Display source documents if available
                    if response["source_documents"]:
                        with st.expander("📄 View Source Documents"):
                            for i, doc in enumerate(response["source_documents"], 1):
                                st.markdown(f"**Source {i}:**")
                                st.write(doc.page_content)
                                st.divider()
            except Exception as e:
                st.error(f"Error getting response: {str(e)}")

if __name__ == "__main__":
    main() 