from datetime import datetime, timezone
from ..extensions import db


class Deck(db.Model):
    __tablename__ = 'decks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100))
    is_public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    flashcards = db.relationship('Flashcard', backref='deck', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_cards=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'subject': self.subject,
            'is_public': self.is_public,
            'user_id': self.user_id,
            'card_count': self.flashcards.count(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_cards:
            data['flashcards'] = [card.to_dict() for card in self.flashcards.all()]
        return data
