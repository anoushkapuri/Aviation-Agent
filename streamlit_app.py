import streamlit as st
import os
from agent import AviationAgent
import tempfile
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

def initialize_agent():
    """Initialize the agent with OpenAI API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return AviationAgent(api_key)

def auto_load_documents():
    """Automatically load documents from the default directory."""
    if st.session_state.agent is None:
        return False
    
    try:
        success = st.session_state.agent.load_documents(directory_path=None)
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
    st.write("Upload aviation planning documents and ask questions about them!")

    # Initialize agent if not already done
    if st.session_state.agent is None:
        try:
            st.session_state.agent = initialize_agent()
        except ValueError as e:
            st.error(str(e))
            return

    # Auto-load documents from default directory if not already attempted
    if not st.session_state.auto_load_attempted and not st.session_state.documents_loaded:
        with st.spinner("Loading pre-existing documents from default directory..."):
            if auto_load_documents():
                st.success("✅ Pre-existing documents loaded successfully! You can now ask questions.")
            else:
                st.warning("⚠️ Could not load pre-existing documents. You can upload files manually or try the button below.")
        st.session_state.auto_load_attempted = True

    # File upload section (still available for additional documents)
    st.subheader("📁 Upload Additional Documents (Optional)")
    st.write("You can upload additional PDF documents if needed. Pre-existing documents are already loaded.")
    
    uploaded_files = st.file_uploader(
        "Upload additional PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    # Button to reload documents from default directory
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔄 Reload Default Documents"):
            with st.spinner("Reloading documents from default directory..."):
                try:
                    success = st.session_state.agent.load_documents(directory_path=None)
                    if success:
                        st.session_state.documents_loaded = True
                        st.success("Documents reloaded successfully!")
                    else:
                        st.error("Failed to reload documents from default directory.")
                except Exception as e:
                    st.error(f"Error reloading documents: {str(e)}")

    # Process uploaded files if any
    if uploaded_files:
        with st.spinner("Processing additional documents..."):
            try:
                # Create a temporary directory to store uploaded files
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Save uploaded files to temporary directory
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                    
                    # Load documents into the agent
                    success = st.session_state.agent.load_documents(directory_path=temp_dir)
                    if success:
                        st.session_state.documents_loaded = True
                        st.success("Additional documents processed successfully!")
                    else:
                        st.error("Failed to process additional documents.")
            except Exception as e:
                st.error(f"Error processing documents: {str(e)}")

    # Chat interface
    st.subheader("💬 Ask questions about the documents")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the documents"):
        if not st.session_state.documents_loaded:
            st.warning("Please wait for documents to load or upload some documents first!")
            return

        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get agent response
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.ask_question(prompt)
                
                # Add assistant message to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
                
                # Display assistant message
                with st.chat_message("assistant"):
                    st.write(response["answer"])
                    
                    # Display source documents if available
                    if response["source_documents"]:
                        with st.expander("View Source Documents"):
                            for doc in response["source_documents"]:
                                st.write(doc.page_content)
            except Exception as e:
                st.error(f"Error getting response: {str(e)}")

if __name__ == "__main__":
    main() 