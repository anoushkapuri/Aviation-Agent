# Aviation Document Analysis Chatbot

This application is an AI-powered chatbot specifically designed for analyzing aviation planning documents. It uses advanced natural language processing and document understanding capabilities to help users extract insights from aviation PDF documents.

## Technical Architecture

The application consists of several key components:

1. **PDF Processor** (`pdf_processor.py`):
   - Handles PDF document processing using PyPDF2
   - Implements text extraction and chunking using LangChain's RecursiveCharacterTextSplitter
   - Creates vector embeddings using OpenAI's embedding model
   - Stores document vectors in a FAISS vector database for efficient similarity search

2. **Aviation Agent** (`agent.py`):
   - Implements a specialized GPT-4 powered agent using LangChain
   - Uses a custom system prompt focused on aviation planning expertise
   - Maintains conversation history and context
   - Provides source document tracking for answers
   - Implements a ConversationalRetrievalChain for intelligent document Q&A

3. **Streamlit Interface** (`streamlit_app.py`):
   - Provides a modern web interface for document interaction
   - **Automatically loads pre-existing documents** from the default directory
   - Supports additional document uploads for enhanced analysis
   - Features a chat-like interface for Q&A
   - Displays source documents for answers

## Features

- **Automatic document loading** - Pre-existing PDFs are loaded automatically
- PDF document processing with intelligent text extraction
- OpenAI GPT-4 powered document analysis
- Interactive chat interface with conversation history
- Support for additional document uploads
- Source document tracking and citation
- Default document directory support
- Both web interface (Streamlit) and CLI modes available

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Aviation-Agent
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install FAISS (vector database):
   - On macOS: `brew install faiss`
   - On Linux: `conda install -c conda-forge faiss-cpu`
   - On Windows: Use the CPU version from conda

5. Create a `.env` file in the project root directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   Get your API key from [OpenAI's website](https://platform.openai.com/api-keys)

6. **Add your PDF documents** to the `test_pdfs` directory (optional):
   - The application comes with sample documents
   - You can add your own aviation PDFs to this directory
   - Documents will be automatically loaded when you start the app

## Running the Application

You can run the application in two modes:

### 1. Web Interface (Streamlit)

```bash
# Method 1: Using the manager script (recommended)
python manager.py
# Select option 2 when prompted

# Method 2: Direct Streamlit run
streamlit run streamlit_app.py
```

The web interface will be available at http://localhost:8501

**✨ New Feature**: Documents are now automatically loaded when you start the app!

### 2. Command Line Interface

```bash
python manager.py
# Select option 1 when prompted
```

## Usage Guide

1. **Web Interface**:
   - Launch the application using one of the methods above
   - **Documents are automatically loaded** - no manual upload required!
   - You can upload additional PDF documents if needed
   - Start asking questions immediately in the chat interface
   - View source documents for answers in the expandable sections

2. **Command Line Interface**:
   - Launch the CLI mode
   - Documents are automatically loaded from the default directory
   - Type your questions and press Enter
   - Type 'exit' to quit

## Default Document Directory

The application uses a `test_pdfs` directory in the project root. **Documents in this directory are automatically loaded** when you start the application, so you don't need to upload them every time.

- **Pre-existing documents**: The app comes with sample aviation documents
- **Add your own**: Place additional PDF files in the `test_pdfs` directory
- **Automatic loading**: No manual intervention required

## Requirements

- Python 3.8 or higher
- OpenAI API key
- FAISS vector database
- PDF documents to analyze (pre-loaded or uploaded)
- Internet connection for API access

## Dependencies

Key dependencies include:
- streamlit==1.32.0
- langchain>=0.1.12
- openai==1.14.0
- PyPDF2==3.0.1
- python-dotenv==1.0.1
- pydantic>=2.6.1

See `requirements.txt` for the complete list.

## Security Notes

- Keep your OpenAI API key secure and never share it publicly
- The `.env` file is automatically ignored by git
- The application runs locally and documents are processed on your machine
- No documents or data are stored permanently on external servers

## Development

The project includes a `.devcontainer` configuration for VS Code and GitHub Codespaces development. It automatically sets up the Python environment and required dependencies. 