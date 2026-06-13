import os
import requests

# 1. HARDCODE YOUR NEW READ TOKEN RIGHT HERE (Bypasses Render's frozen memory cache)
# Replace the text below with your real token that starts with hf_...
HF_API_TOKEN = "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"

def generate_reply(prompt):
    # GPT2: The most stable, universally open model on the entire platform
    url = "https://huggingface.co"
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        # If the token works, it will return code 200 instantly!
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data:
                raw_text = data["generated_text"]
                return raw_text.replace(prompt, "").strip()
                
        return f"API Status Notice: Server returned error code {response.status_code}"

    except Exception as e:
        return f"API Connection error: {e}"
