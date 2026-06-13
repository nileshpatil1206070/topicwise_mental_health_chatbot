import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")

MODEL_ID = "google/gemma-4-31B-it"

# Create the working client connection
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
        # Added a 120-second timeout to give the server plenty of time to wake up!
        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7,
            timeout=120  
        )
        
        # Using YOUR working line of code!
        if response and response.choices:
            return response.choices[0].message.content
        return "System Notice: The model sent back an empty response. Please try again."
        
    except Exception as e:
        # If the server is genuinely down or overloaded, return the error text
        return f"Error: {e}"
