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

def initialize_agent():
    """Initialize the agent with OpenAI API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return AviationAgent(api_key)

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

    # File upload
    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    # Add a button to load documents from default directory
    if st.button("Load Documents from Default Directory"):
        with st.spinner("Loading documents from default directory..."):
            try:
                success = st.session_state.agent.load_documents(directory_path=None)
                if success:
                    st.session_state.documents_loaded = True
                    st.success("Documents loaded successfully from default directory!")
                else:
                    st.error("Failed to load documents from default directory.")
            except Exception as e:
                st.error(f"Error loading documents: {str(e)}")

    if uploaded_files:
        with st.spinner("Processing documents..."):
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
                        st.success("Documents processed successfully!")
                    else:
                        st.error("Failed to process documents.")
            except Exception as e:
                st.error(f"Error processing documents: {str(e)}")

    # Chat interface
    st.subheader("Ask questions about the documents")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the documents"):
        if not st.session_state.documents_loaded:
            st.warning("Please load documents first (either upload files or use the default directory)!")
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