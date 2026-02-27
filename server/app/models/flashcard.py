from datetime import datetime, timezone
from ..extensions import db


class Flashcard(db.Model):
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    hint = db.Column(db.Text, default='')
    difficulty = db.Column(db.String(10), default='Medium')
    topic = db.Column(db.String(200))
    section = db.Column(db.String(200))
    image_url = db.Column(db.String(500))
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'hint': self.hint or '',
            'difficulty': self.difficulty,
            'topic': self.topic,
            'section': self.section,
            'image_url': self.image_url,
            'deck_id': self.deck_id,
            'created_at': self.created_at.isoformat(),
        }
