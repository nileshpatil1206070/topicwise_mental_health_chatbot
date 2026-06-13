import os
import requests

#google/gemma-4-31B-it

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "google/gemma-4-31B-it")

import os
import requests
from dotenv import load_dotenv

# 1. Load the environment variables from your .env file
load_dotenv()

# 2. Make sure your variable names match what is inside your .env file!
HF_API_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HF_API_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "google/gemma-4-31B-it")

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# 1. Load your secret Hugging Face token
load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")

# 2. Point to the Gemma-4 model repository
MODEL_ID = "google/gemma-4-31B-it"

# 3. Create the working API client connection
client = InferenceClient(model=MODEL_ID, token=hf_token)

def generate_reply(prompt):
    # Format the prompt in the exact image-text list structure Gemma-4 requires
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
        # Send the chat completion request via the client
        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        # Return the clean text response
        return response.choices[0].message.content
        
    except Exception as e:
        return f"An error occurred: {e}"

# 4. Get input from the user and print answer trial 
#question = input("Please ask a question: \n")
#answer = generate_reply(question)

#print("\n--- Gemma-4 Response ---")
#print(answer)
