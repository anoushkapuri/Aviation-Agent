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
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except Exception as e:
        print(f"Error launching Streamlit app: {str(e)}")

def run_cli():
    """Run the command-line interface version."""
    # Get OpenAI API key from environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    # Initialize the aviation agent
    agent = AviationAgent(openai_api_key)
    
    # Load documents from the default PDF directory
    success = agent.load_documents(directory_path=None)  # None will use the default directory
    if not success:
        print("Failed to load documents from default directory.")
        return
    
    print("PDF processing complete! You can now ask questions about the documents.")
    print("Type 'exit' to quit the conversation.")
    
    while True:
        question = input("\nYour question: ").strip()
        if question.lower() == 'exit':
            break
            
        try:
            response = agent.ask_question(question)
            print("\nAnswer:", response["answer"])
            print("\nSource documents used:", len(response["source_documents"]))
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    print("Aviation Document Analysis")
    print("1. Run Command Line Interface")
    print("2. Launch Streamlit Web Interface")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        run_cli()
    elif choice == "2":
        run_streamlit_app()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main() 