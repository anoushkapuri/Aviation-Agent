#!/usr/bin/env python3
"""
Test script to load PDF from test_pdfs directory and verify functionality
"""
import os
from dotenv import load_dotenv
from agent import AviationAgent

def test_pdf_loading():
    """Test loading PDF from test_pdfs directory"""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    print("🔑 API key found")
    
    try:
        # Initialize agent
        print("🤖 Initializing Aviation Agent...")
        agent = AviationAgent(api_key)
        print("✅ Agent initialized successfully")
        
        # Load documents from default directory (test_pdfs)
        print("📚 Loading documents from test_pdfs directory...")
        success = agent.load_documents(directory_path=None)
        
        if success:
            print("✅ Documents loaded successfully!")
            
            # Test asking a question
            print("❓ Testing question answering...")
            response = agent.ask_question("What is this document about?")
            
            print("📝 Response:")
            print(response["answer"])
            
            if response["source_documents"]:
                print(f"📄 Found {len(response['source_documents'])} source documents")
            
            return True
        else:
            print("❌ Failed to load documents")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing PDF Loading Functionality")
    print("=" * 50)
    
    success = test_pdf_loading()
    
    if success:
        print("\n🎉 All tests passed! The PDF loading is working correctly.")
        print("You can now use the Streamlit app at http://localhost:8501")
    else:
        print("\n💥 Tests failed. Please check the error messages above.") 