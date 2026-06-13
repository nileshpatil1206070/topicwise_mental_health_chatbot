import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")

# Primary choice model
MODEL_ID = "google/gemma-4-31B-it"

# 1. Initialize our primary connection client
client = InferenceClient(model=MODEL_ID, token=hf_token)

def generate_reply(prompt):
    messages = [
        {
            "role": "user", 
            "content": [
                {
                    "type": "text", 
                    "text": prompt
                }
            ]
        }
    ]
    
    try:
        # Try talking to Gemma-4 with a safe 30-second wait window
        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7,
            timeout=30  
        )
        return response.choices[0].message.content
        
    except Exception as primary_error:
        print(f"Gemma-4 busy or asleep: {primary_error}. Switching to backup instantly...")
        
        try:
            # 2. BACKUP ROUTE: If Gemma-4 takes too long, use Qwen2.5-72B (incredibly fast & free)
            backup_client = InferenceClient(model="Qwen/Qwen2.5-72B-Instruct", token=hf_token)
            backup_response = backup_client.chat_completion(
                messages=messages,
                max_tokens=200,
                temperature=0.7,
                timeout=30
            )
            return backup_response.choices[0].message.content
            
        except Exception as backup_error:
            # If both servers are fully locked down, return a clean error code for app.py
            return f"Error: Servers unavailable. Details: {backup_error}"
