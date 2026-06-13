import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Automatically reads your universal READ token from Render
hf_token = os.getenv("HF_API_TOKEN")

def generate_reply(prompt):
    if not hf_token:
        return "System Notification: API token is missing in your deployment environment settings."

    # Three highly active, open-source models that run on the free tier
    MODELS_TO_TRY = [
        "Qwen/Qwen2.5-7B-Instruct",
        "google/gemma-2-2b-it",
        "microsoft/Phi-3-mini-4k-instruct"
    ]
    
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    # Unified template layout to guarantee clean text compatibility across all endpoints
    payload = {
        "inputs": f"<|user|>\n{prompt}</s>\n<|assistant|>\n",
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7
        },
        "options": {
            "wait_for_model": True  # Instructs the server to wake up the selected model if idle
        }
    }

    # Automatically switches down the line if any engine returns a 403 or server error
    for model_path in MODELS_TO_TRY:
        url = f"https://huggingface.co{model_path}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            # If the model is active and responds, return the answer immediately
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0 and "generated_text" in data:
                    raw_text = data["generated_text"]
                    
                    # Strip formatting tags cleanly out of the conversation loop
                    if "<|assistant|>\n" in raw_text:
                        return raw_text.split("<|assistant|>\n")[-1].strip()
                    return raw_text.replace(prompt, "").strip()
            
            # Log the issue silently in your Render console and fall through to the next choice
            print(f"Server skipped {model_path} with status code: {response.status_code}")
            
        except Exception as e:
            print(f"Network request connection failed for {model_path}: {e}")
            continue

    # Final fallback text message if the entire Hugging Face free pipeline faces downtime
    return "The system is currently adjusting its AI server connections. Please wait 10 seconds and try sending your message again."
