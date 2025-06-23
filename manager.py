#Import the relevant modules needed to run the file
import os
import sys
import subprocess
from agent import AviationAgent
from dotenv import load_dotenv

load_dotenv()

def run_streamlit_app():
    """Launch the Streamlit app."""
    try:
        print("🚀 Launching Streamlit web interface...")
        print("📚 Pre-existing documents will be automatically loaded!")
        print("🌐 The app will open in your browser at http://localhost:8501")
        print("⏳ Please wait a moment for the app to start...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except Exception as e:
        print(f"Error launching Streamlit app: {str(e)}")

def run_cli():
    """Run the command-line interface version."""
    # Get OpenAI API key from environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    print("🤖 Initializing Aviation Agent...")
    # Initialize the aviation agent
    agent = AviationAgent(openai_api_key)
    
    print("📚 Loading pre-existing documents from default directory...")
    # Load documents from the default PDF directory
    success = agent.load_documents(directory_path=None)  # None will use the default directory
    if not success:
        print("❌ Failed to load documents from default directory.")
        return
    
    print("✅ PDF processing complete! You can now ask questions about the documents.")
    print("💡 Type 'exit' to quit the conversation.")
    print("📄 Available documents: Check the 'test_pdfs' directory for loaded files.")
    
    while True:
        question = input("\n❓ Your question: ").strip()
        if question.lower() == 'exit':
            print("👋 Goodbye!")
            break
            
        try:
            response = agent.ask_question(question)
            print("\n🤖 Answer:", response["answer"])
            print(f"📄 Source documents used: {len(response['source_documents'])}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def main():
    print("✈️ Aviation Document Analysis")
    print("=" * 40)
    print("📚 Pre-existing documents are available in the 'test_pdfs' directory")
    print("🔄 Documents will be automatically loaded when you start the application")
    print("=" * 40)
    print("1. Run Command Line Interface")
    print("2. Launch Streamlit Web Interface")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        run_cli()
    elif choice == "2":
        run_streamlit_app()
    else:
        print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main() 