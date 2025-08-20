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
import argparse


def get_api_key() -> Optional[str]:
    """Get the Gemini API key from environment variables"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        return None
    return api_key


def get_openai_api_key() -> Optional[str]:
    """Get the OpenAI API key from environment variables"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        return None
    return api_key


def read_context_file(context_file: str) -> Optional[str]:
    """Read the context from a file"""
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading context file: {e}", file=sys.stderr)
        return None


def send_prompt_to_gemini_requests(prompt: str, api_key: str, context: str = None, use_system_instruction: bool = False) -> Optional[str]:
    """Send a prompt to the Gemini API using requests and return the response"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key={api_key}"
    system_instruction = (
        "You are an experienced psychologist, helping businesses understand their employees' behavior in terms of work and productivity. "
        "You are also an experienced project manager in the software development field for a long time, providing consultations on how to make software teams more productive. "
        "Also, you have a knack on word puzzles, text pattern analysis, and forensic level of information extraction from seemingly difficult to understand texts from different sources. "
        "You can speak and understand both English and Japanese, but you prefer to use English for your responses. "
        "For each team member, summarize their activities in a narrative, paragraph-style format. Do not use bullet points or lists for activities; instead, aggregate and describe each member's activities as a short story or paragraph. "
        "Keep the breakdown by team member, but make each activity summary flow naturally. Do not mention anything about your expertise, just provide the summary based on the context provided. "
        "Respond in a neutral tone, without any personal opinions or biases. Do not use any emojis in your response. "
        "Do not address your response to the user themselves, but to someone else generic. The generated report must be in HTML do not use markdown or plain text formatting. Don't include a header."
    )
    if use_system_instruction:
        # REST API: system instruction and context as separate messages, only 'parts' (no 'role')
        contents = []
        contents.append({"parts": [{"text": system_instruction}]})
        if context:
            contents.append({"parts": [{"text": context}]})
        payload = {
            "contents": contents
        }
    else:
        # Ordinary prompt mode: just context and prompt
        parts = []
        if context:
            parts.append({"text": context})
        if prompt:
            parts.append({"text": prompt})
        payload = {
            "contents": [
                {
                    "parts": parts
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


def send_prompt_to_gemini_genai(prompt: str, api_key: str, context: str = None, use_system_instruction: bool = False) -> Optional[str]:
    """Send a prompt to the Gemini API using google-generativeai (best practice) and return the response"""
    try:
        import google.generativeai as genai
    except ImportError:
        print("Error: google-generativeai package is not installed. Please install it with 'pip install google-generativeai'", file=sys.stderr)
        return None

    genai.configure(api_key=api_key)

    system_instruction = (
        "You are an experienced psychologist, helping businesses understand their employees' behavior in terms of work and productivity. "
        "You are also an experienced project manager in the software development field for a long time, providing consultations on how to make software teams more productive. "
        "Also, you have a knack on word puzzles, text pattern analysis, and forensic level of information extraction from seemingly difficult to understand texts from different sources. "
        "You can speak and understand both English and Japanese, but you prefer to use English for your responses. "
        "For each team member, summarize their activities in a narrative, paragraph-style format. Do not use bullet points or lists for activities; instead, aggregate and describe each member's activities as a short story or paragraph. "
        "Keep the breakdown by team member, but make each activity summary flow naturally. Do not mention anything about your expertise, just provide the summary based on the context provided. "
        "Respond in a neutral tone, without any personal opinions or biases. Do not use any emojis in your response. "
        "Do not address your response to the user themselves, but to someone else generic. The generated report must be in HTML do not use markdown or plain text formatting. Don't include a header."
    )
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-001",
            system_instruction=system_instruction if use_system_instruction else None
        )

        full_prompt = []
        if context:
            full_prompt.append("Context:\n" + context)
        if prompt:
            full_prompt.append(prompt)
        final_content = "\n\n".join(full_prompt)

        response = model.generate_content(final_content)
        if hasattr(response, 'text'):
            return response.text
        if hasattr(response, 'result'):
            return str(response.result)
        print("Error: Unexpected response format from genai GenerativeModel API", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error using google-generativeai GenerativeModel API: {e}", file=sys.stderr)
        return None


def send_prompt_to_chatgpt(prompt: str, api_key: str, context: str = None) -> Optional[str]:
    """Send a prompt to the ChatGPT API and return the response"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = []
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": prompt})
    payload = {
        "model": "gpt-4",
        "messages": messages
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"Error making request to OpenAI API: {http_err}", file=sys.stderr)
            try:
                print(f"OpenAI API response: {response.text}", file=sys.stderr)
            except Exception:
                pass
            return None
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        print("Error: Unexpected response format from OpenAI API", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error making request to OpenAI API: {e}", file=sys.stderr)
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
    parser = argparse.ArgumentParser(description="ai-py: CLI for Gemini and OpenAI (ChatGPT)")
    parser.add_argument('--use-genai', action='store_true', help='Use google-generativeai package instead of requests')
    parser.add_argument('--prompt', type=str, help='Prompt to send to Gemini (if not provided, reads from stdin)')
    parser.add_argument('--use-context', action='store_true', help='Use context.txt as context and a default system instruction for Gemini 2.0')
    parser.add_argument('--use-chatgpt', action='store_true', help='Use OpenAI ChatGPT API instead of Gemini')
    args = parser.parse_args()

    if args.use_chatgpt:
        api_key = get_openai_api_key()
    else:
        api_key = get_api_key()
    if not api_key:
        sys.exit(1)

    context = None
    prompt = None
    use_system_instruction = False
    if args.use_context:
        context = read_context_file('context.txt')
        if context is None:
            print("Error: context.txt not found or unreadable.", file=sys.stderr)
            sys.exit(1)
        use_system_instruction = True
        # No prompt in use-context mode
    elif args.prompt is not None:
        prompt = args.prompt.strip()
    else:
        prompt = read_prompt_from_stdin()
    if not args.use_context and not prompt:
        sys.exit(1)

    print("Sending prompt to AI...", file=sys.stderr)

    if args.use_chatgpt:
        response = send_prompt_to_chatgpt(prompt, api_key, context)
    elif args.use_context:
        response = send_prompt_to_gemini_genai(prompt, api_key, context, use_system_instruction=use_system_instruction)
    elif args.use_genai:
        response = send_prompt_to_gemini_genai(prompt, api_key, context, use_system_instruction=use_system_instruction)
    else:
        response = send_prompt_to_gemini_requests(prompt, api_key, context, use_system_instruction=use_system_instruction)

    if response:
        print("\n" + "="*50)
        print("AI Response:")
        print("="*50)
        print(response)
    else:
        print("Failed to get response from AI", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
