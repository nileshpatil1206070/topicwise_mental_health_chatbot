import os
import requests
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")

# A highly stable, fast, always-available 7B model on the free tier
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"

def generate_reply(prompt):
    # Formats the text directly into the standard prompt structure
    formatted_prompt = f"<|user|>\n{prompt}</s>\n<|assistant|>\n"
    
    url = f"https://huggingface.co{MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "return_full_text": False
        },
        "options": {
            "wait_for_model": True  # Safely wakes up the model if it's asleep
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # If Hugging Face returns an error, catch it safely
        if response.status_code != 200:
            return f"Error: Server returned status code {response.status_code}"
            
        data = response.json()
        
        # Extract the clean generated text response out of the standard list format
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            return data[0]["generated_text"].strip()
            
        return "Error: Unexpected response format from Hugging Face."
        
    except Exception as e:
        return f"Error: Request failed. Details: {e}"
