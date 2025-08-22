import os
import asyncio
import httpx

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise RuntimeError('GEMINI_API_KEY environment variable not set')

ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent'
HEADERS = {'Content-Type': 'application/json'}
PARAMS = {'key': API_KEY}

prompt1 = "A" * 5000
prompt2 = "B" * 5000

async def send_prompt(client, prompt, idx):
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = await client.post(ENDPOINT, params=PARAMS, json=data, headers=HEADERS)
        r.raise_for_status()
        print(f"[Task {idx}] {r.status_code} {r.text}")
    except Exception as e:
        print(f"[Task {idx}] Error: {e}")

async def main():
    async with httpx.AsyncClient(http2=True, timeout=60) as client:
        await asyncio.gather(
            send_prompt(client, prompt1, 1),
            send_prompt(client, prompt2, 2)
        )

if __name__ == "__main__":
    asyncio.run(main())
    # Print loaded OpenSSL library paths from /proc/self/maps
    print("Loaded OpenSSL libraries:")
    try:
        with open("/proc/self/maps") as f:
            for line in f:
                if "ssl" in line and ".so" in line:
                    print(line.strip())
    except Exception as e:
        print(f"Could not read /proc/self/maps: {e}")