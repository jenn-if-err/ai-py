import os
import threading
import httpx

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise RuntimeError('GEMINI_API_KEY environment variable not set')

ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent'
HEADERS = {'Content-Type': 'application/json'}
PARAMS = {'key': API_KEY}

prompt1 = "A" * 5000
prompt2 = "B" * 5000

def send_prompt(client, prompt, idx):
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = client.post(ENDPOINT, params=PARAMS, json=data, headers=HEADERS)
        r.raise_for_status()
        print(f"[Thread {idx}] {r.status_code} {r.text}")
    except Exception as e:
        print(f"[Thread {idx}] Error: {e}")

def main():
    with httpx.Client(http2=True, timeout=60) as client:
        t1 = threading.Thread(target=send_prompt, args=(client, prompt1, 1))
        t2 = threading.Thread(target=send_prompt, args=(client, prompt2, 2))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

if __name__ == "__main__":
    main()