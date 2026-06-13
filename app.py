import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_apscheduler import APScheduler  
# 1. Import the background scheduler

# Import db directly from models.py
from models import db, Topic, ChatMessage
from hf_chat import generate_reply

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

# --- FIX: FORCES AN ABSOLUTE DIRECTORY PATH ---
# Finds your root folder path automatically on Render's cloud servers
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Pins app.db to that exact absolute folder layout explicitly
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", 
    f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
)
# ----------------------------------------------

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# 2. Define the background automated wiping task
def auto_wipe_database():
    """Drops and resets all SQL tables automatically on a fixed timer loop."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("⏰ [Scheduler]: 5 minutes elapsed. Complete database and chat history wiped successfully.")

# 3. Initialize and configure the scheduler
scheduler = APScheduler()

with app.app_context():
    db.create_all()
    
    # 4. Schedule the job to trigger exactly every 30 minutes
    scheduler.add_job(
        id='database_wipe_job',
        func=auto_wipe_database,
        trigger='interval',
        minutes=5
    )
    # Start the background scheduler thread
    scheduler.start()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        topic_name = request.form.get("topic", "").strip()
        if topic_name:
            existing = Topic.query.filter_by(name=topic_name).first()
            if not existing:
                db.session.add(Topic(name=topic_name))
                db.session.commit()
                flash("Topic added successfully.")
            else:
                flash("Topic already exists.")
        return redirect(url_for("home"))

    topics = Topic.query.order_by(Topic.id.desc()).all()
    return render_template("index.html", topics=topics)

@app.route("/delete-topic/<int:topic_id>", methods=["POST"])
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    ChatMessage.query.filter_by(topic_id=topic_id).delete()
    db.session.delete(topic)
    db.session.commit()
    flash("Topic deleted.")
    return redirect(url_for("home"))

@app.route("/reset", methods=["POST"])
def reset_workspace():
    db.drop_all()
    db.create_all()
    flash("Workspace completely reset.")
    return redirect(url_for("home"))

@app.route("/chat/<int:topic_id>", methods=["GET", "POST"])
def chat(topic_id):
    topic = Topic.query.get_or_404(topic_id)

    if request.method == "POST":
        user_msg = request.form.get("message", "").strip()
        if user_msg:
            # 1. Save user question
            db.session.add(ChatMessage(role="user", content=user_msg, topic_id=topic.id))
            db.session.commit()

            # 2. Get AI Reply from hf_chat.py
            prompt = f"You are a supportive mental health demo assistant. if topic not related to mental health , simply say , ask related to mental health topics. only and only answer related to mental health topics. Topic: {topic.name}. User: {user_msg}. Reply kindly and briefly."
            bot_reply = generate_reply(prompt)

            # --- REMOVED THE GENERIC SYSTEM NOTICE BLINDFOLD ---
            # If bot_reply is completely empty or missing, provide a simple placeholder
            if not bot_reply:
                bot_reply = "System Notice: The backend function returned an empty string."
            # ---------------------------------------------------

            # 3. Save the exact text string to the database
            db.session.add(ChatMessage(role="assistant", content=bot_reply, topic_id=topic.id))
            db.session.commit()

        return redirect(url_for("chat", topic_id=topic.id))

    messages = ChatMessage.query.filter_by(topic_id=topic.id).order_by(ChatMessage.id.asc()).all()
    return render_template("chat.html", topic=topic, messages=messages)


if __name__ == "__main__":
    app.run(debug=True)
