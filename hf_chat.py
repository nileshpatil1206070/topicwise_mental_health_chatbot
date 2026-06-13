import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")

# Primary choice model
MODEL_ID = "google/gemma-4-31B-it"
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
        # Try talking to Gemma-4
        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7,
            timeout=30  
        )
        
        # FIX: Try accessing via object attributes, fallback to dictionary style indexing if needed
        if hasattr(response, "choices") and response.choices:
            choice = response.choices[0]
            if hasattr(choice, "message"):
                return choice.message.content
            return choice["message"]["content"]
            
        return "System Notice: The model sent back an empty response. Please try again."
        
    except Exception as primary_error:
        print(f"Gemma-4 issue: {primary_error}. Switching to backup instantly...")
        
        try:
            # BACKUP ROUTE: Using the ultra-stable, lightning-fast Qwen model endpoint
            backup_client = InferenceClient(model="Qwen/Qwen3.6-35B-A3B", token=hf_token)
            backup_response = backup_client.chat_completion(
                messages=messages,
                max_tokens=200,
                temperature=0.7,
                timeout=30
            )
            
            if hasattr(backup_response, "choices") and backup_response.choices:
                choice = backup_response.choices[0]
                if hasattr(choice, "message"):
                    return choice.message.content
                return choice["message"]["content"]
                
            return "System Notice: Backup model sent empty text."
            
        except Exception as backup_error:
            return f"Error: Both servers unavailable. Details: {backup_error}"
