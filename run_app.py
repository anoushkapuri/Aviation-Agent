#!/usr/bin/env python3
"""
Simple script to launch the Streamlit app
"""
import subprocess
import sys
import os

def main():
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Launch streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except KeyboardInterrupt:
        print("\nApp stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error launching app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 