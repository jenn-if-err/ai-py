#!/usr/bin/env python3
"""
Test script to verify the environment is set up correctly
"""

import os
import sys

def test_environment():
    """Test if the environment is properly configured"""
    print("Testing environment setup...")
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("GEMINI_API_KEY is set")
        print(f"  Key length: {len(api_key)} characters")
        print(f"  Starts with: {api_key[:10]}...")
    else:
        print("GEMINI_API_KEY is not set")
        print("  Please set your Gemini API key:")
        print("  $env:GEMINI_API_KEY=\"your_api_key_here\"")
        return False
    
    # Test imports
    try:
        import requests
        print("requests library is available")
        print(f"  Version: {requests.__version__}")
    except ImportError:
        print("requests library is not installed")
        return False
    
    print("\nEnvironment is ready!")
    print("\nTo test the CLI app, run:")
    print("Get-Content example_prompt.txt | python main.py")
    return True

if __name__ == "__main__":
    if not test_environment():
        sys.exit(1)
