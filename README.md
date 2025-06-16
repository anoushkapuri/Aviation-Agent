# Aviation Document Analysis Chatbot

This application allows you to analyze aviation planning documents using AI. You can upload PDF documents and ask questions about their content.

## Features

- PDF document processing and text extraction
- OpenAI embeddings for document analysis
- Interactive chat interface
- Support for multiple document uploads
- Source document tracking for answers

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual OpenAI API key from [OpenAI's website](https://platform.openai.com/api-keys)

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the provided local URL (usually http://localhost:8501)
3. Upload one or more PDF documents
4. Start asking questions about the documents!

## Requirements

- Python 3.8 or higher
- OpenAI API key
- PDF documents to analyze

## Note

Make sure to keep your OpenAI API key secure and never share it publicly. The `.env` file should be added to your `.gitignore` to prevent accidentally committing it to version control. 