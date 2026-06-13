import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Safely reads your environment variable from Render
hf_token = os.getenv("HF_API_TOKEN")

def generate_reply(prompt):
    if not hf_token:
        return "System Notification: API token is missing in your deployment environment settings."

    # A fast, highly reliable model endpoint for free text queries
    url = "https://huggingface.co"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    # Formatted using a pure text prompt setup to keep the server connection light
    payload = {
        "inputs": f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        },
        "options": {
            "wait_for_model": True  # Instructs the server to wake the model up if it is asleep
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # If the response returns a list, extract the text string cleanly
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                raw_text = data[0]["generated_text"]
                # Clean up the system tags so only the actual answer shows
                if "<|im_start|>assistant\n" in raw_text:
                    return raw_text.split("<|im_start|>assistant\n")[-1].strip()
                return raw_text.strip()

        # ─── SECURE BACKUP MODEL ───
        # If the primary model is busy, automatically switch to Llama 3.2
        fallback_url = "https://huggingface.co"
        fallback_res = requests.post(fallback_url, headers=headers, json=payload, timeout=20)
        
        if fallback_res.status_code == 200:
            fdata = fallback_res.json()
            if isinstance(fdata, list) and len(fdata) > 0 and "generated_text" in fdata[0]:
                f_text = fdata[0]["generated_text"]
                if "<|im_start|>assistant\n" in f_text:
                    return f_text.split("<|im_start|>assistant\n")[-1].strip()
                return f_text.strip()
                
        return f"API Status Notice: Server busy. Code {response.status_code}"

    except Exception as e:
        return f"API Connection error: {e}"
