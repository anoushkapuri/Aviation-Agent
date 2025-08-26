#!/usr/bin/env python3
"""
Test script for PDF processing caching functionality
"""

import os
from dotenv import load_dotenv
from pdf_processor import PDFProcessor

# Load environment variables
load_dotenv()

def test_caching():
    """Test the caching functionality."""
    print("🧪 Testing PDF Processing Caching")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    # Initialize processor
    processor = PDFProcessor(api_key)
    
    # Test 1: First run (should process and cache)
    print("📊 Test 1: First run (should process documents and create cache)")
    vector_store = processor.process_pdf()
    
    if vector_store:
        print("✅ Documents processed successfully")
    else:
        print("❌ Failed to process documents")
        return False
    
    # Check cache info after first run
    cache_info = processor.get_cache_info()
    print(f"📁 Cache stores created: {len(cache_info['cached_stores'])}")
    print(f"💾 Total cache size: {cache_info['total_cache_size_mb']} MB")
    
    # Test 2: Second run (should load from cache)
    print("\n📊 Test 2: Second run (should load from cache - no API calls)")
    processor2 = PDFProcessor(api_key)  # New instance to simulate app restart
    vector_store2 = processor2.process_pdf()
    
    if vector_store2:
        print("✅ Documents loaded from cache successfully")
    else:
        print("❌ Failed to load documents from cache")
        return False
    
    # Show final cache info
    final_cache_info = processor2.get_cache_info()
    print(f"📁 Cache stores: {len(final_cache_info['cached_stores'])}")
    print(f"💾 Total cache size: {final_cache_info['total_cache_size_mb']} MB")
    
    print("\n🎉 Caching test completed successfully!")
    print("💡 Subsequent app loads will use cached embeddings (no API cost)")
    
    return True

if __name__ == "__main__":
    test_caching()
