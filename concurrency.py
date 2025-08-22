import socket
import ssl
import threading
import time
import os
import google.generativeai as genai

HOST = os.getenv('AI_SERVER_HOST', '127.0.0.1')  # Set your Gemini/gemini-proxy host
PORT = int(os.getenv('AI_SERVER_PORT', '443'))   # Set your Gemini/gemini-proxy port
API_KEY = os.getenv('GEMINI_API_KEY')

# Two large prompts for concurrency test
prompt1 = "J" * 5000
prompt2 = "T" * 5000
chunk_size = 1000

def send_prompt(sock, prompt, delay):
    for i in range(0, len(prompt), chunk_size):
        chunk = prompt[i:i+chunk_size].encode()
        sock.sendall(chunk)
        time.sleep(delay)

def main():
    if not API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set")
        return
    try:
        # TLS connection (change to socket.create_connection for plain TCP)
        raw_sock = socket.create_connection((HOST, PORT))
        sock = ssl.create_default_context().wrap_socket(raw_sock, server_hostname=HOST)
        print(f"Connected to {HOST}:{PORT} (TLS)")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return
    try:
        t1 = threading.Thread(target=send_prompt, args=(sock, prompt1, 0.05))
        t2 = threading.Thread(target=send_prompt, args=(sock, prompt2, 0.05))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        try:
            sock.settimeout(2)
            response = sock.recv(4096)
            print("Response:", response)
        except Exception:
            print("No response or read timeout.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
