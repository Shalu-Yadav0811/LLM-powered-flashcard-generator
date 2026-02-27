from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.flashcard import Flashcard
from ..models.deck import Deck

flashcards_bp = Blueprint('flashcards', __name__)


@flashcards_bp.route('/<int:card_id>', methods=['PUT'])
@jwt_required()
def update_card(card_id):
    user_id = int(get_jwt_identity())
    card = Flashcard.query.get_or_404(card_id)

    # Verify ownership through the deck
    deck = Deck.query.get(card.deck_id)
    if not deck or deck.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()

    if 'question' in data:
        card.question = data['question'].strip()
    if 'answer' in data:
        card.answer = data['answer'].strip()
    if 'difficulty' in data:
        if data['difficulty'] in ['Easy', 'Medium', 'Hard']:
            card.difficulty = data['difficulty']
    if 'topic' in data:
        card.topic = data['topic']
    if 'section' in data:
        card.section = data['section']

    db.session.commit()
    return jsonify({'flashcard': card.to_dict()})


@flashcards_bp.route('/<int:card_id>', methods=['DELETE'])
@jwt_required()
def delete_card(card_id):
    user_id = int(get_jwt_identity())
    card = Flashcard.query.get_or_404(card_id)

    # Verify ownership through the deck
    deck = Deck.query.get(card.deck_id)
    if not deck or deck.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403

    db.session.delete(card)
    db.session.commit()
    return jsonify({'message': 'Flashcard deleted'})
