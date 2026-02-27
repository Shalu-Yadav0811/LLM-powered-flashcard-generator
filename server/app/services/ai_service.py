import json
import re
import base64
import google.generativeai as genai
from flask import current_app


def configure_genai():
    """Configure the Gemini API with the app's API key."""
    api_key = current_app.config['GOOGLE_API_KEY']
    if not api_key:
        raise ValueError('Google API key not configured in environment')
    genai.configure(api_key=api_key)


def detect_sections(content):
    """Detect structure (headings/chapters) in the content."""
    section_pattern = re.compile(
        r'^(#+|\d+\.|[A-Z][a-z]+:|Chapter \d+|Section \d+)', re.MULTILINE
    )
    sections = []
    structured_lines = []

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if section_pattern.match(line):
            sections.append(line)
            structured_lines.append(f'\n=== {line} ===\n')
        else:
            structured_lines.append(line)

    return sections, '\n'.join(structured_lines)


def build_prompt(content, subject, sections, structured_content,
                 num_cards=15, difficulty_filter=None, include_hints=False):
    """Build the Gemini prompt for flashcard generation."""
    # Hint field
    hint_instruction = ""
    hint_format = ""
    if include_hints:
        hint_instruction = '- Each flashcard must also have a "hint" field: a short clue (1 sentence) to help recall the answer without giving it away'
        hint_format = ',\n  "hint": "A brief clue to help recall the answer"'

    # Section handling
    if sections:
        structure_info = (
            f"\n\nThe content is organized into the following sections: "
            f"{', '.join(sections)}. For each flashcard, include a 'section' "
            f"field indicating the section it belongs to."
        )
        section_field = "- Each flashcard must have: question, answer, difficulty, topic, section"
        return_format = (
            '{\n  "question": "What is...?",\n  "answer": "The answer explanation...",'
            '\n  "difficulty": "Medium",\n  "topic": "Main topic",'
            f'\n  "section": "Section heading or chapter name"{hint_format}\n}}'
        )
    else:
        structure_info = ""
        section_field = "- Each flashcard must have: question, answer, difficulty, topic"
        return_format = (
            '{\n  "question": "What is...?",\n  "answer": "The answer explanation...",'
            f'\n  "difficulty": "Medium",\n  "topic": "Main topic"{hint_format}\n}}'
        )

    # Difficulty filter
    difficulty_instruction = '- Difficulty must be exactly "Easy", "Medium", or "Hard"'
    if difficulty_filter and difficulty_filter in ['Easy', 'Medium', 'Hard']:
        difficulty_instruction = f'- ALL flashcards must have difficulty set to exactly "{difficulty_filter}"'

    return f"""You are an expert educational content creator. Generate exactly {num_cards} high-quality flashcards from the following {subject} content.

STRICT FORMAT REQUIREMENTS:
- Return ONLY a valid JSON array
{section_field}
{difficulty_instruction}
{hint_instruction}
- Questions should be clear and concise
- Answers should be comprehensive but not too long
- Cover different aspects of the content
- Ensure factual accuracy
- IMPORTANT: Return ONLY the JSON array, no other text, explanation, or markdown formatting
{structure_info}

Content:
{structured_content}

Return format (JSON array only):
[
  {return_format}
]"""


def parse_flashcard_response(response_text, sections, include_hints=False):
    """Parse and validate the Gemini JSON response."""
    # Clean markdown code block markers
    text = response_text.strip()
    text = text.replace('```json', '').replace('```', '').strip()

    # Find JSON array
    start_idx = text.find('[')
    end_idx = text.rfind(']') + 1

    if start_idx == -1 or end_idx == 0:
        raise ValueError('No valid JSON array found in response')

    json_str = text[start_idx:end_idx]

    # Clean whitespace
    json_str = re.sub(r'\s+', ' ', json_str.replace('\n', ' ').replace('\r', ' ').replace('\t', ' '))
    json_str = json_str.lstrip('\ufeff').lstrip()

    try:
        flashcards = json.loads(json_str)
    except json.JSONDecodeError:
        # Try cleaning escape characters
        json_str = json_str.replace('\\n', ' ').replace('\\r', ' ').replace('\\t', ' ')
        json_str = re.sub(r'\\+', '\\\\', json_str)
        flashcards = json.loads(json_str)

    # Validate structure
    for card in flashcards:
        if not all(key in card for key in ['question', 'answer', 'difficulty', 'topic']):
            raise ValueError('Invalid flashcard structure - missing required fields')
        if card['difficulty'] not in ['Easy', 'Medium', 'Hard']:
            card['difficulty'] = 'Medium'
        if sections and 'section' not in card:
            card['section'] = 'Unknown'
        if include_hints and 'hint' not in card:
            card['hint'] = ''

    return flashcards


def generate_flashcards(content, subject, num_cards=15,
                        difficulty_filter=None, include_hints=False):
    """Generate flashcards from content using Gemini AI."""
    configure_genai()

    sections, structured_content = detect_sections(content)
    prompt = build_prompt(
        content, subject, sections, structured_content,
        num_cards, difficulty_filter, include_hints,
    )

    # Scale max tokens based on card count and hints
    max_tokens = max(2048, num_cards * 200)
    if include_hints:
        max_tokens = int(max_tokens * 1.3)

    model = genai.GenerativeModel('gemini-1.5-flash')
    generation_config = {
        'temperature': 0.7,
        'top_p': 0.8,
        'top_k': 40,
        'max_output_tokens': max_tokens,
    }

    response = model.generate_content(prompt, generation_config=generation_config)
    return parse_flashcard_response(response.text, sections, include_hints)


def regenerate_single_card(content, subject, existing_card):
    """Regenerate a single flashcard with a different question/answer."""
    configure_genai()

    prompt = f"""You are an expert educational content creator. A student wants a DIFFERENT flashcard to replace an existing one.

Existing card to replace:
- Question: {existing_card.get('question', '')}
- Answer: {existing_card.get('answer', '')}

Generate exactly 1 NEW flashcard from the following {subject} content. The new card must cover a DIFFERENT aspect of the content than the card above.

STRICT FORMAT REQUIREMENTS:
- Return ONLY a valid JSON object (NOT an array)
- Must have: question, answer, difficulty, topic
- Difficulty must be exactly "Easy", "Medium", or "Hard"
- IMPORTANT: Return ONLY the JSON object, no other text

Content:
{content}

Return format:
{{"question": "...", "answer": "...", "difficulty": "Medium", "topic": "..."}}"""

    model = genai.GenerativeModel('gemini-1.5-flash')
    generation_config = {
        'temperature': 0.9,
        'top_p': 0.9,
        'top_k': 40,
        'max_output_tokens': 512,
    }

    response = model.generate_content(prompt, generation_config=generation_config)
    text = response.text.strip().replace('```json', '').replace('```', '').strip()

    # Try parsing as object
    start = text.find('{')
    end = text.rfind('}') + 1
    if start == -1 or end == 0:
        raise ValueError('No valid JSON object found in response')

    card = json.loads(text[start:end])
    if card['difficulty'] not in ['Easy', 'Medium', 'Hard']:
        card['difficulty'] = 'Medium'
    return card


def generate_from_image(image_bytes, image_mime, subject, num_cards=5, include_hints=False):
    """Generate flashcards from an image using Gemini Vision."""
    configure_genai()

    hint_instruction = ""
    hint_format = ""
    if include_hints:
        hint_instruction = '- Each flashcard must also have a "hint" field: a short clue (1 sentence)'
        hint_format = ', "hint": "A brief clue"'

    prompt = f"""You are an expert educational content creator. Analyze this image and generate exactly {num_cards} high-quality flashcards about its {subject} content.

STRICT FORMAT REQUIREMENTS:
- Return ONLY a valid JSON array
- Each flashcard must have: question, answer, difficulty, topic
{hint_instruction}
- Difficulty must be exactly "Easy", "Medium", or "Hard"
- Questions should be clear and concise
- IMPORTANT: Return ONLY the JSON array, no other text

Return format (JSON array only):
[
  {{"question": "What is...?", "answer": "...", "difficulty": "Medium", "topic": "..."{hint_format}}}
]"""

    model = genai.GenerativeModel('gemini-1.5-flash')
    generation_config = {
        'temperature': 0.7,
        'top_p': 0.8,
        'top_k': 40,
        'max_output_tokens': 2048,
    }

    image_part = {
        'mime_type': image_mime,
        'data': base64.b64encode(image_bytes).decode('utf-8'),
    }

    response = model.generate_content(
        [prompt, image_part],
        generation_config=generation_config,
    )
    return parse_flashcard_response(response.text, sections=[], include_hints=include_hints)


def search_answer(content, question, flashcards=None):
    """Search for an answer in flashcards or content using Gemini."""
    # First check existing flashcards
    if flashcards:
        question_lower = question.lower()
        for card in flashcards:
            if question_lower in card.get('question', '').lower():
                return card.get('answer', '')
            if question_lower in card.get('answer', '').lower():
                return card.get('answer', '')

    if not content:
        return None

    configure_genai()

    prompt = f"""As an advanced AI assistant, your task is to precisely extract and provide the answer to the user's question SOLELY based on the following content.

Instructions:
1. If the answer is explicitly found in the content, provide it directly without any additional commentary or introductory phrases.
2. If the answer is NOT present in the content, respond with: "Sorry, the answer is not present in the provided content."
3. Do not invent information or use external knowledge.

Content:
{content}

Question: {question}

Answer:"""

    model = genai.GenerativeModel('gemini-1.5-flash')
    generation_config = {
        'temperature': 0.2,
        'top_p': 0.8,
        'top_k': 40,
        'max_output_tokens': 512,
    }

    response = model.generate_content(prompt, generation_config=generation_config)
    return response.text.strip()
