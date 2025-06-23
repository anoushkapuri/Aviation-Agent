import streamlit as st
import os
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
            if auto_load_documents():
                st.success("✅ Documents loaded successfully! You can now ask questions.")
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