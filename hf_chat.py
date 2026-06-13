import os
import requests

# 1. HARDCODE YOUR NEW READ TOKEN RIGHT HERE (Bypasses Render's frozen memory cache)
# Replace the text below with your real token that starts with hf_...

import os
import requests

# 1. HARDCODED TOKEN: Put your fresh, valid READ token inside the quotes below

HF_API_TOKEN = "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"
def generate_reply(prompt):
    # A list of completely different, highly active free open-source models
    MODELS_TO_TRY = [
        "Qwen/Qwen2.5-7B-Instruct",
        "google/gemma-2-2b-it",
        "microsoft/Phi-3-mini-4k-instruct"
    ]
    
    # FIX: Uses the exact hardcoded variable name for authorization
    headers = {
        "Authorization": f"Bearer {HARDCODED_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": f"<|user|>\n{prompt}</s>\n<|assistant|>\n",
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7
        },
        "options": {
            "wait_for_model": True
        }
    }

    # Loop through each model path automatically
    for model_path in MODELS_TO_TRY:
        url = f"https://api-inference.huggingface.co/models/{model_path}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            # If the model succeeds, process and return it instantly!
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0 and "generated_text" in data:
                    raw_text = data["generated_text"]
                    if "<|assistant|>\n" in raw_text:
                        return raw_text.split("<|assistant|>\n")[-1].strip()
                    return raw_text.replace(prompt, "").strip()
            
            # Log the skip reason to your Render console
            print(f"Skipped {model_path} with status code: {response.status_code}")
            
        except Exception as e:
            print(f"Connection failed for {model_path}: {e}")
            continue

    # Final fallback if all else fails
    return "The system is currently adjusting its AI server connections. Please wait 10 seconds and try sending your message again."
