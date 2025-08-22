import os
import threading
import requests

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise RuntimeError('GEMINI_API_KEY environment variable not set')

# Use the same endpoint as main.py
ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent'
HEADERS = {
    'Content-Type': 'application/json',
}


prompt1 = "J" * 5000
prompt2 = "T" * 5000

def send_prompt(prompt, idx):
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    params = {"key": API_KEY}
    try:
        response = requests.post(ENDPOINT, headers=HEADERS, params=params, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        print(f"[Thread {idx}] Response: {data}")
    except Exception as e:
        print(f"[Thread {idx}] Error: {e}")

def main():
    t1 = threading.Thread(target=send_prompt, args=(prompt1, 1))
    t2 = threading.Thread(target=send_prompt, args=(prompt2, 2))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()