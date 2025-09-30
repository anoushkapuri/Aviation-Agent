#!/usr/bin/env python3
"""
Demo script for the enhanced Aviation Intelligence Platform
Run this to start the professional demonstration interface
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Aviation Intelligence Platform Demo...")
    print("=" * 50)
    print("📋 Features:")
    print("  ✨ Professional dark theme")
    print("  🎨 Smooth animations and transitions")
    print("  📊 Real-time system metrics")
    print("  💬 Enhanced chat interface")
    print("  🔒 Professional branding")
    print("=" * 50)
    print("🌐 The application will open in your browser...")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Demo stopped. Thank you for using Aviation Intelligence Platform!")
    except Exception as e:
        print(f"❌ Error starting demo: {e}")

if __name__ == "__main__":
    main()
