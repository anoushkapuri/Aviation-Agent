#!/usr/bin/env python3
"""
Test Streamlit caching functionality
"""

import streamlit as st
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_streamlit_caching():
    """Test the Streamlit caching implementation."""
    st.title("🧪 Streamlit Caching Test")
    
    # Import here to avoid issues
    from streamlit_app import initialize_agent, get_pdf_files_hash, load_documents_cached
    
    st.write("Testing if Streamlit caching prevents repeated processing...")
    
    # Test 1: PDF Hash
    st.subheader("📊 Test 1: PDF Files Hash")
    pdf_hash = get_pdf_files_hash()
    st.write(f"PDF Hash: `{pdf_hash}`")
    st.success("✅ PDF hash generated successfully")
    
    # Test 2: Agent Initialization
    st.subheader("🤖 Test 2: Agent Initialization (Cached)")
    start_time = time.time()
    try:
        agent = initialize_agent()
        init_time = time.time() - start_time
        st.write(f"⏱️ Agent initialization time: {init_time:.2f} seconds")
        if init_time < 1.0:
            st.success("⚡ Agent loaded from cache!")
        else:
            st.info("🔄 Agent initialized fresh")
    except Exception as e:
        st.error(f"❌ Error initializing agent: {e}")
        return
    
    # Test 3: Document Loading
    st.subheader("📚 Test 3: Document Loading (Cached)")
    if st.button("Test Document Loading"):
        start_time = time.time()
        try:
            success = load_documents_cached(agent, pdf_hash)
            load_time = time.time() - start_time
            
            st.write(f"⏱️ Document loading time: {load_time:.2f} seconds")
            
            if success:
                if load_time < 2.0:
                    st.success("⚡ Documents loaded from Streamlit cache! (No API costs)")
                else:
                    st.warning("🔄 Documents processed fresh (API costs incurred)")
            else:
                st.error("❌ Failed to load documents")
                
        except Exception as e:
            st.error(f"❌ Error loading documents: {e}")
    
    # Cache status
    st.subheader("📊 Cache Status")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("PDF Hash", pdf_hash[:8] + "...")
        
    with col2:
        if 'documents_loaded' in st.session_state and st.session_state.documents_loaded:
            st.metric("Documents Status", "✅ Loaded")
        else:
            st.metric("Documents Status", "❌ Not Loaded")

if __name__ == "__main__":
    test_streamlit_caching()
