import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Automatically reads your universal READ token from Render
hf_token = os.getenv("HF_API_TOKEN")

def generate_reply(prompt):
    if not hf_token:
        return "System Notification: API token is missing in your deployment environment settings."

    # GPT2: The most stable, universally available text model on the free cluster
    url = "https://huggingface.co"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    # Simple direct text payload (No complex structural formatting tokens)
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data:
                raw_text = data["generated_text"]
                # Clean up the original prompt text from the returned output
                return raw_text.replace(prompt, "").strip()
                
        return f"API Status Notice: Server returned error code {response.status_code}"

    except Exception as e:
        return f"API Connection error: {e}"
