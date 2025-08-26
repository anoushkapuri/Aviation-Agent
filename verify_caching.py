#!/usr/bin/env python3
"""
Quick script to verify caching is working properly
"""

import os
import time
from dotenv import load_dotenv
from pdf_processor import PDFProcessor

# Load environment variables
load_dotenv()

def verify_caching():
    """Verify that caching is working properly."""
    print("🔍 Verifying Caching Implementation")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        return False
    
    # Test 1: First run timing
    print("📊 Test 1: First run (may use cache if available)")
    start_time = time.time()
    processor = PDFProcessor(api_key)
    vector_store = processor.process_pdf()
    first_run_time = time.time() - start_time
    
    if not vector_store:
        print("❌ Failed to process documents")
        return False
    
    print(f"⏱️  First run completed in: {first_run_time:.2f} seconds")
    
    # Check cache info
    cache_info = processor.get_cache_info()
    print(f"📁 Cache stores available: {len(cache_info['cached_stores'])}")
    print(f"💾 Total cache size: {cache_info['total_cache_size_mb']} MB")
    
    if len(cache_info['cached_stores']) == 0:
        print("⚠️  No cache found - this was the first processing")
        print("🔄 Run this script again to see caching in action")
        return True
    
    # Test 2: Second run (should be much faster)
    print("\n📊 Test 2: Second run (should load from cache)")
    start_time = time.time()
    processor2 = PDFProcessor(api_key)
    vector_store2 = processor2.process_pdf()
    second_run_time = time.time() - start_time
    
    print(f"⏱️  Second run completed in: {second_run_time:.2f} seconds")
    
    # Compare times
    speedup = first_run_time / second_run_time if second_run_time > 0 else float('inf')
    print(f"🚀 Speed improvement: {speedup:.1f}x faster")
    
    # Verification results
    print("\n🎯 Verification Results:")
    if second_run_time < 2.0:  # Should be very fast if cached
        print("✅ CACHING WORKING: Second run was very fast (< 2 seconds)")
        print("💰 This means NO OpenAI API calls on subsequent loads")
    else:
        print("⚠️  Second run was slow - may not be using cache properly")
    
    if speedup > 5:
        print("✅ EXCELLENT: Cache provides significant speed improvement")
    elif speedup > 2:
        print("✅ GOOD: Cache provides noticeable speed improvement")
    else:
        print("⚠️  Speed improvement unclear - check implementation")
    
    return True

def check_cache_files():
    """Check if cache files exist on disk."""
    print("\n📂 Cache File Verification:")
    cache_dir = "vector_cache"
    
    if not os.path.exists(cache_dir):
        print("❌ Cache directory doesn't exist")
        return False
    
    cache_items = os.listdir(cache_dir)
    if not cache_items:
        print("📭 Cache directory is empty (no documents cached yet)")
        return False
    
    print(f"📁 Found {len(cache_items)} cache items:")
    for item in cache_items:
        item_path = os.path.join(cache_dir, item)
        if os.path.isdir(item_path):
            files = os.listdir(item_path)
            print(f"   📦 {item}/ contains {len(files)} files")
    
    return True

if __name__ == "__main__":
    verify_caching()
    check_cache_files()
    
    print("\n💡 How to interpret results:")
    print("   ✅ Fast second run (< 2 sec) = Caching working")
    print("   🚀 Speed improvement > 5x = Excellent caching")
    print("   📁 Cache directory with files = Cache persisted")
    print("   💰 Fast subsequent runs = No API costs!")
