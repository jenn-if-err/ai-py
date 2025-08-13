import os
import sys
import argparse
from typing import Optional, List

# Gemini (google-generativeai) chat function
def gemini_chat(history: List[str], api_key: str) -> Optional[str]:
    try:
        from google import genai
    except ImportError:
        print("Error: google-generativeai package is not installed. Please install it with 'pip install google-generativeai'", file=sys.stderr)
        return None
    try:
        client = genai.Client()
        model = "gemini-2.0-flash-001"
        response = client.models.generate_content(model=model, contents=history)
        if hasattr(response, 'text'):
            return response.text
        if hasattr(response, 'result'):
            return str(response.result)
        print("Error: Unexpected response format from genai Client API", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error using google-generativeai Client API: {e}", file=sys.stderr)
        return None

# OpenAI ChatGPT chat function
def chatgpt_chat(history: List[dict], api_key: str) -> Optional[str]:
    import requests
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": history
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        print("Error: Unexpected response format from OpenAI API", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error making request to OpenAI API: {e}", file=sys.stderr)
        return None

def get_gemini_api_key() -> Optional[str]:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        return None
    return api_key

def get_openai_api_key() -> Optional[str]:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        return None
    return api_key

def main():
    parser = argparse.ArgumentParser(description="ai-py Chatbot CLI (Gemini or ChatGPT)")
    parser.add_argument('--use-chatgpt', action='store_true', help='Use OpenAI ChatGPT API instead of Gemini')
    args = parser.parse_args()

    print("Welcome to ai-py Chatbot CLI! Type 'exit' or 'quit' to end the session.\n")
    if args.use_chatgpt:
        api_key = get_openai_api_key()
        if not api_key:
            sys.exit(1)
        history = []
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            history.append({"role": "user", "content": user_input})
            print("ChatGPT: ...", end="\r")
            response = chatgpt_chat(history, api_key)
            if response:
                print(f"ChatGPT: {response}")
                history.append({"role": "assistant", "content": response})
            else:
                print("ChatGPT: [No response]")
    else:
        api_key = get_gemini_api_key()
        if not api_key:
            sys.exit(1)
        history = []
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            history.append(user_input)
            print("Gemini: ...", end="\r")
            response = gemini_chat(history, api_key)
            if response:
                print(f"Gemini: {response}")
                history.append(response)
            else:
                print("Gemini: [No response]")

if __name__ == "__main__":
    main()
