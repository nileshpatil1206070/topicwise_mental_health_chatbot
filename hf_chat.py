import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")

# SWAPPED TO: An ultra-stable, fast, free-tier friendly text model
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
client = InferenceClient(model=MODEL_ID, token=hf_token)

def generate_reply(prompt):
    messages = [
        {
            "role": "user", 
            "content": prompt  # Using a cleaner string format to bypass object validation limits
        }
    ]
    
    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=250,
            temperature=0.7,
            timeout=20  
        )
        
        if response and response.choices:
            return response.choices[0].message.content
            
        return "Error: Empty response object received."
        
    except Exception as e:
        print(f"Primary API Error: {e}")
        try:
            # FALLBACK: Swapping instantly to another ultra-reliable text engine
            fallback_client = InferenceClient(model="meta-llama/Llama-3.2-3B-Instruct", token=hf_token)
            fallback_response = fallback_client.chat_completion(
                messages=messages,
                max_tokens=250,
                temperature=0.7,
                timeout=20
            )
            if fallback_response and fallback_response.choices:
                return fallback_response.choices[0].message.content
            return "Error: Fallback returned empty object."
        except Exception as fallback_err:
            return f"Error: All free servers busy. Details: {fallback_err}"
