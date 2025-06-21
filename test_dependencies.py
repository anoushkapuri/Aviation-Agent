#!/usr/bin/env python3
"""
Test script to verify dependencies work correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all required imports work correctly."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import streamlit as st
        print("✓ streamlit imported successfully")
        
        from langchain_openai import ChatOpenAI
        print("✓ langchain_openai imported successfully")
        
        from langchain.chains import ConversationalRetrievalChain
        print("✓ ConversationalRetrievalChain imported successfully")
        
        from langchain.memory import ConversationBufferMemory
        print("✓ ConversationBufferMemory imported successfully")
        
        from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
        print("✓ LangChain prompts imported successfully")
        
        from langchain_community.embeddings import OpenAIEmbeddings
        print("✓ OpenAIEmbeddings imported successfully")
        
        from langchain_community.vectorstores import FAISS
        print("✓ FAISS imported successfully")
        
        import PyPDF2
        print("✓ PyPDF2 imported successfully")
        
        print("\nAll imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def test_openai_client():
    """Test OpenAI client initialization."""
    try:
        print("\nTesting OpenAI client...")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            return False
            
        from langchain_openai import ChatOpenAI
        
        # Test client initialization
        llm = ChatOpenAI(
            temperature=0.3,
            openai_api_key=api_key,
            model_name="gpt-4o-mini"
        )
        print("✓ OpenAI client initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI client error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Aviation AI Dependencies")
    print("=" * 40)
    
    imports_ok = test_imports()
    openai_ok = test_openai_client()
    
    if imports_ok and openai_ok:
        print("\n🎉 All tests passed! Dependencies are working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.") 