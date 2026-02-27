from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.deck import Deck
from ..models.flashcard import Flashcard

decks_bp = Blueprint('decks', __name__)


@decks_bp.route('', methods=['GET'])
@jwt_required()
def list_decks():
    user_id = int(get_jwt_identity())
    decks = Deck.query.filter_by(user_id=user_id).order_by(Deck.updated_at.desc()).all()
    return jsonify({'decks': [deck.to_dict() for deck in decks]})


@decks_bp.route('', methods=['POST'])
@jwt_required()
def create_deck():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    deck = Deck(
        title=title,
        description=data.get('description', ''),
        subject=data.get('subject', ''),
        is_public=data.get('is_public', False),
        user_id=user_id,
    )

    db.session.add(deck)
    db.session.commit()

    return jsonify({'deck': deck.to_dict()}), 201


@decks_bp.route('/<int:deck_id>', methods=['GET'])
@jwt_required()
def get_deck(deck_id):
    user_id = int(get_jwt_identity())
    deck = Deck.query.get_or_404(deck_id)

    if deck.user_id != user_id and not deck.is_public:
        return jsonify({'error': 'Access denied'}), 403

    return jsonify({'deck': deck.to_dict(include_cards=True)})


@decks_bp.route('/<int:deck_id>', methods=['PUT'])
@jwt_required()
def update_deck(deck_id):
    user_id = int(get_jwt_identity())
    deck = Deck.query.get_or_404(deck_id)

    if deck.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()

    if 'title' in data:
        deck.title = data['title'].strip()
    if 'description' in data:
        deck.description = data['description']
    if 'subject' in data:
        deck.subject = data['subject']
    if 'is_public' in data:
        deck.is_public = data['is_public']

    db.session.commit()
    return jsonify({'deck': deck.to_dict()})


@decks_bp.route('/<int:deck_id>', methods=['DELETE'])
@jwt_required()
def delete_deck(deck_id):
    user_id = int(get_jwt_identity())
    deck = Deck.query.get_or_404(deck_id)

    if deck.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403

    db.session.delete(deck)
    db.session.commit()
    return jsonify({'message': 'Deck deleted'})


@decks_bp.route('/<int:deck_id>/cards', methods=['POST'])
@jwt_required()
def add_card_to_deck(deck_id):
    user_id = int(get_jwt_identity())
    deck = Deck.query.get_or_404(deck_id)

    if deck.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json()

    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()

    if not question or not answer:
        return jsonify({'error': 'Question and answer are required'}), 400

    card = Flashcard(
        question=question,
        answer=answer,
        difficulty=data.get('difficulty', 'Medium'),
        topic=data.get('topic', ''),
        section=data.get('section', ''),
        deck_id=deck_id,
    )

    db.session.add(card)
    db.session.commit()

    return jsonify({'flashcard': card.to_dict()}), 201
