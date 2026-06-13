import os
import requests
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HF_API_TOKEN")

def generate_reply(prompt):
    if not hf_token:
        return "Error: HF_API_TOKEN not found."

    MODELS_TO_TRY = [
        "Qwen/Qwen2.5-7B-Instruct",
        "google/gemma-2-2b-it",
        "microsoft/Phi-3-mini-4k-instruct"
    ]

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    error_log = []

    for model in MODELS_TO_TRY:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }

        try:
            response = requests.post(
                "https://router.huggingface.co/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()

                if (
                    "choices" in data
                    and len(data["choices"]) > 0
                    and "message" in data["choices"][0]
                ):
                    return data["choices"][0]["message"]["content"].strip()

            error_log.append(
                f"[{model}] HTTP {response.status_code}: {response.text[:500]}"
            )

        except Exception as e:
            error_log.append(
                f"[{model}] Exception: {str(e)}"
            )

    return (
        "ALL MODELS FAILED\n\n" +
        "\n\n".join(error_log)
    )
