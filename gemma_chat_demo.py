import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# 1. Load your secret Hugging Face token
load_dotenv()
hf_token = os.getenv("HF_API_TOKEN")

# 2. Point to the Gemma-4 model repository
MODEL_ID = "google/gemma-4-31B-it"

# 3. Create the API client connection
client = InferenceClient(model=MODEL_ID, token=hf_token)

# 4. Create your chat prompt 
# Note: Gemma-4 expects content as a list of dictionaries because it supports images!
messages = [
    {
        "role": "user", 
        "content": [
            {
                "type": "text", 
                "text": "What are the causes of digital revolution answer in brief para?"
            }
        ]
    }
]

print("Connecting to Gemma-4-31B-it serverless API...")

try:
    # 5. Send request to Hugging Face servers
    response = client.chat_completion(
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )
    
    # 6. Print out the AI's text answer
    print("\n--- Gemma-4 Response ---")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\nAn error occurred: {e}")
