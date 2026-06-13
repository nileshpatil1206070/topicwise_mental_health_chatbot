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
        # 1. Try fetching response from Gemma-4
        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7,
            timeout=25  # Give Gemma 25 seconds before switching
        )
        
        # Exact object path syntax required by huggingface_hub
        if response and response.choices:
            return response.choices[0].message.content
            
        return "Error: Primary model returned an empty choice object."
        
    except Exception as primary_error:
        # This will now safely trigger if Gemma-4 is asleep or times out
        print(f"Gemma-4 fallback triggered! Reason: {primary_error}")
        
        try:
            # 2. BACKUP ROUTE: Fallback to the ultra-fast Qwen model instantly
            backup_client = InferenceClient(model="Qwen/Qwen3.6-35B-A3B", token=hf_token)
            backup_response = backup_client.chat_completion(
                messages=messages,
                max_tokens=200,
                temperature=0.7,
                timeout=25
            )
            
            if backup_response and backup_response.choices:
                return backup_response.choices[0].message.content
                
            return "Error: Backup model returned an empty choice object."
            
        except Exception as backup_error:
            # If both servers fail completely, return an explicit trace message
            return f"Error: Both API models timed out. Details: {backup_error}"
