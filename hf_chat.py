import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Securely reads the token from Render's hidden environment variables
hf_token = os.getenv("HF_API_TOKEN")

def generate_reply(prompt):
    if not hf_token:
        return "Python Error: The environment variable 'HF_API_TOKEN' is empty or not found on Render."

    # Three highly active, stable open-source models on the free tier
    MODELS_TO_TRY = [
        "Qwen/Qwen2.5-7B-Instruct",
        "google/gemma-2-2b-it",
        "microsoft/Phi-3-mini-4k-instruct"
    ]
    
    headers = {
        "Authorization": f"Bearer {hf_token}",
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

    # Tracking errors across each attempted endpoint
    error_log = []

    for model_path in MODELS_TO_TRY:
        url = f"https://huggingface.co{model_path}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            # If the model succeeds, return it instantly
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0 and "generated_text" in data:
                    raw_text = data["generated_text"]
                    if "<|assistant|>\n" in raw_text:
                        return raw_text.split("<|assistant|>\n")[-1].strip()
                    return raw_text.replace(prompt, "").strip()
            
            # Record the exact raw server response text if status code is not 200
            error_log.append(f"[{model_path}] Code {response.status_code}: {response.text}")
            
        except Exception as e:
            error_log.append(f"[{model_path}] Connection Exception: {str(e)}")
            continue

    # Returns the absolute raw output logs if every model in the loop fails
    return "ALL MODELS FAILED. Raw Server Responses:\n\n" + "\n\n".join(error_log)
