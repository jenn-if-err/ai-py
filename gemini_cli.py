#!/usr/bin/env python3
"""
Simple CLI app to send prompts to Gemini AI API
Reads prompt from stdin and displays the response
"""

import os
import sys
import json
import requests
from typing import Optional


def get_api_key() -> Optional[str]:
    """Get the Gemini API key from environment variables"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        return None
    return api_key


def send_prompt_to_gemini(prompt: str, api_key: str) -> Optional[str]:
    """
    Send a prompt to the Gemini API and return the response
    
    Args:
        prompt: The user's prompt to send to Gemini
        api_key: The API key for authentication
        
    Returns:
        The AI response or None if there was an error
    """
    # gemini API endpoint 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    #request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status() 
        
        data = response.json()
        
        # extract the generated text from the response
        if 'candidates' in data and len(data['candidates']) > 0:
            if 'content' in data['candidates'][0] and 'parts' in data['candidates'][0]['content']:
                return data['candidates'][0]['content']['parts'][0]['text']
        
        print("Error: Unexpected response format from API", file=sys.stderr)
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Gemini API: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        return None
    except KeyError as e:
        print(f"Error: Missing key in response: {e}", file=sys.stderr)
        return None


def read_prompt_from_stdin() -> Optional[str]:
    """Read the prompt from stdin"""
    try:
        if sys.stdin.isatty():
            # prompt user with platform-specific instructions
            if os.name == 'nt':  # Windows
                print("Enter your prompt (press Ctrl+Z then Enter on Windows to finish):")
            else:  # Unix/Linux/WSL
                print("Enter your prompt (press Ctrl+D on Unix/Linux/WSL to finish):")
        
        prompt = sys.stdin.read().strip()
        if not prompt:
            print("Error: No prompt provided", file=sys.stderr)
            return None
        return prompt
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading from stdin: {e}", file=sys.stderr)
        return None


def main():

    api_key = get_api_key()
    if not api_key:
        sys.exit(1)
    
    # read prompt from stdin
    prompt = read_prompt_from_stdin()
    if not prompt:
        sys.exit(1)
    
    print("Sending prompt to Gemini AI...", file=sys.stderr)
    
    # send prompt to Gemini API
    response = send_prompt_to_gemini(prompt, api_key)
    if response:
        print("\n" + "="*50)
        print("AI Response:")
        print("="*50)
        print(response)
    else:
        print("Failed to get response from Gemini AI", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
