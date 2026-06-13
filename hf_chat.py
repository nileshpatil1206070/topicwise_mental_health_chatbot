import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Automatically reads your environment variable token from Render
hf_token = os.getenv("HF_API_TOKEN")

def generate_reply(prompt):
    if not hf_token:
        return "System Notification: API token is missing in your deployment environment settings."

    # Zephyr-7B: Fully open, public, non-gated model. Never throws a 403 error.
    url = "https://huggingface.co"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    # Formatted explicitly using Zephyr's exact system prompt syntax layout structure
    payload = {
        "inputs": f"<|user|>\n{prompt}</s>\n<|assistant|>\n",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        },
        "options": {
            "wait_for_model": True  # Instructs the server to wake up the model files if idle
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data:
                raw_text = data[0]["generated_text"]
                # Strip out the prompt tags cleanly so only the actual answer shows
                if "<|assistant|>\n" in raw_text:
                    return raw_text.split("<|assistant|>\n")[-1].strip()
                return raw_text.strip()
                
        # Fallback to a second completely open, public model if Zephyr is overloaded
        backup_url = "https://huggingface.co"
        backup_res = requests.post(backup_url, headers=headers, json={"inputs": prompt}, timeout=20)
        if backup_res.status_code == 200:
            b_data = backup_res.json()
            if isinstance(b_data, list) and len(b_data) > 0 and "generated_text" in b_data:
                return b_data[0]["generated_text"].replace(prompt, "").strip()

        return f"API Status Notice: Server returned error code {response.status_code}"

    except Exception as e:
        return f"API Connection error: {e}"
