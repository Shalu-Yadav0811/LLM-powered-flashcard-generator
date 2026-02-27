from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.deck import Deck
from ..models.flashcard import Flashcard
from ..services.ai_service import generate_flashcards, search_answer
from ..services.pdf_service import extract_text_from_pdf
from ..services.translate_service import translate_text

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate():
    """Generate flashcards from content and optionally save to a deck."""
    try:
        # Extract content from file or JSON
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            if uploaded_file.filename.endswith('.pdf'):
                content = extract_text_from_pdf(uploaded_file.stream)
            elif uploaded_file.filename.endswith('.txt'):
                content = uploaded_file.stream.read().decode('utf-8')
            else:
                return jsonify({'error': 'Unsupported file type. Only PDF and TXT are supported.'}), 400

            subject = request.form.get('subject', 'General')
            deck_id = request.form.get('deck_id')
            num_cards = int(request.form.get('num_cards', 15))
        else:
            data = request.get_json()
            content = data.get('content')
            subject = data.get('subject', 'General')
            deck_id = data.get('deck_id')
            num_cards = data.get('num_cards', 15)

        if not content:
            return jsonify({'error': 'No content provided'}), 400

        # Generate flashcards with AI
        cards = generate_flashcards(content, subject, num_cards)

        # If a deck_id is provided, save cards to the deck
        if deck_id:
            user_id = int(get_jwt_identity())
            deck = Deck.query.get(int(deck_id))

            if not deck or deck.user_id != user_id:
                return jsonify({'error': 'Deck not found or access denied'}), 404

            saved_cards = []
            for card_data in cards:
                card = Flashcard(
                    question=card_data['question'],
                    answer=card_data['answer'],
                    difficulty=card_data.get('difficulty', 'Medium'),
                    topic=card_data.get('topic', ''),
                    section=card_data.get('section', ''),
                    deck_id=deck.id,
                )
                db.session.add(card)
                saved_cards.append(card)

            db.session.commit()
            return jsonify({
                'flashcards': [c.to_dict() for c in saved_cards],
                'content': content,
            })

        return jsonify({'flashcards': cards, 'content': content})

    except Exception as e:
        return jsonify({'error': f'Failed to generate flashcards: {str(e)}'}), 500


@ai_bp.route('/search-answer', methods=['POST'])
@jwt_required()
def search():
    """Search for an answer within content or flashcards."""
    try:
        data = request.get_json()
        content = data.get('content')
        question = data.get('question')
        flashcards = data.get('flashcards', [])

        if not content and not flashcards:
            return jsonify({'error': 'Missing content or flashcards to search in'}), 400
        if not question:
            return jsonify({'error': 'Missing question'}), 400

        answer = search_answer(content, question, flashcards)

        if answer is None:
            return jsonify({'error': 'Sorry, the answer is not present in the provided content.'}), 200

        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/translate', methods=['POST'])
@jwt_required()
def translate():
    """Translate text to a target language."""
    try:
        data = request.get_json()
        text = data.get('text')
        target_lang = data.get('targetLang')

        if not text or not target_lang:
            return jsonify({'error': 'Missing text or targetLang'}), 400

        translated = translate_text(text, target_lang)
        return jsonify({'translated': translated})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
