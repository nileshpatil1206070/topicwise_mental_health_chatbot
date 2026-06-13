from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=False)
    topic = db.relationship("Topic", backref=db.backref("messages", lazy=True))