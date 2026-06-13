this app is deployed on render:
link: https://nills-topicwise-mental-health-chatbot.onrender.com/
# Mental Health Bot

A simple Flask-based mental health chatbot that helps users discuss mental health topics in a supportive and friendly way.

## Features

* Create and manage mental health topics
* Chat with an AI-powered assistant
* Store conversation history per topic
* Reset workspace manually as well as automatically
* Built with Flask, SQLite, and Hugging Face AI

## Setup

1. Clone the repository
2. Create a `.env` file and add your API keys
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. Open `http://localhost:5000` in your browser

## Environment Variables

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///app.db
HF_API_KEY=your_huggingface_api_key
```

## Disclaimer

This project is for educational and demonstration purposes only and is not a substitute for professional mental health support.
