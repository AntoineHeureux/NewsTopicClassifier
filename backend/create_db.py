from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ArticleResult(db.Model):
    __tablename__ = "article_results"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2083), nullable=False)
    title = db.Column(db.String(512))
    summary = db.Column(db.Text)
    topic = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)