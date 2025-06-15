from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
import nltk
import json
import re
import requests
import PyPDF2

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_url_path='')
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit for uploads

# Download required NLTK data
nltk.download('punkt')

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# List available models
available_models = [model.name for model in genai.list_models()]
print("Available models:", available_models)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate_flashcards():
    try:
        # Check if a file was uploaded
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            if uploaded_file and uploaded_file.filename.endswith('.pdf'):
                content = extract_text_from_pdf(uploaded_file.stream)
            elif uploaded_file and uploaded_file.filename.endswith('.txt'):
                content = uploaded_file.stream.read().decode('utf-8')
            else:
                return jsonify({'error': 'Unsupported file type. Only PDF and TXT are supported.'}), 400
        else:
            # If no file, expect content directly in JSON
            data = request.json
            content = data.get('content')

        subject = request.form.get('subject') if 'file' in request.files else data.get('subject')

        if not content:
            return jsonify({'error': 'No content provided'}), 400

        if not GOOGLE_API_KEY:
            return jsonify({'error': 'Google API key not configured in environment'}), 500
        
        try:
            flashcards = generate_with_gemini(content, subject)
            return jsonify({'flashcards': flashcards, 'content': content})
        except Exception as e:
            error_message = str(e)
            print("Error in generate_with_gemini:", error_message)  # Debug print
            return jsonify({'error': f'Failed to generate flashcards: {error_message}'}), 500

    except Exception as e:
        error_message = str(e)
        print("Error in generate_flashcards:", error_message)  # Debug print
        return jsonify({'error': f'Server error: {error_message}'}), 500

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text() or ""
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def generate_with_gemini(content, subject):
    # Detect structure: find subheadings/chapters (lines starting with #, ##, or similar)
    section_pattern = re.compile(r'^(#+|\d+\.|[A-Z][a-z]+:|Chapter \d+|Section \d+)', re.MULTILINE)
    sections = []
    current_section = None
    structured_content = []
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if section_pattern.match(line):
            current_section = line
            sections.append(current_section)
            structured_content.append(f"\n=== {current_section} ===\n")
        else:
            structured_content.append(line)
    structured_content_str = '\n'.join(structured_content)
    
    # Build structure info for the prompt
    if sections:
        structure_info = f"\n\nThe content is organized into the following sections: {', '.join(sections)}. For each flashcard, include a 'section' field indicating the section it belongs to."
        section_field = "- Each flashcard must have: question, answer, difficulty, topic, section"
        return_format = '{\n  "question": "What is...?",\n  "answer": "The answer explanation...",\n  "difficulty": "Medium",\n  "topic": "Main topic",\n  "section": "Section heading or chapter name"\n}'
    else:
        structure_info = ""
        section_field = "- Each flashcard must have: question, answer, difficulty, topic"
        return_format = '{\n  "question": "What is...?",\n  "answer": "The answer explanation...",\n  "difficulty": "Medium",\n  "topic": "Main topic"\n}'

    prompt = f"""You are an expert educational content creator. Generate exactly 15 high-quality flashcards from the following {subject} content. 

STRICT FORMAT REQUIREMENTS:
- Return ONLY a valid JSON array
{section_field}
- Difficulty must be exactly \"Easy\", \"Medium\", or \"Hard\"
- Questions should be clear and concise
- Answers should be comprehensive but not too long
- Cover different aspects of the content
- Ensure factual accuracy
- IMPORTANT: Return ONLY the JSON array, no other text, explanation, or markdown formatting
{structure_info}

Content:
{structured_content_str}

Return format (JSON array only):
[
  {return_format}
]"""

    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Configure generation parameters
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        # Generate content with specific configuration
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Get the response text
        response_text = response.text.strip()
        print("Raw Gemini response:", response_text)  # Debug print
        
        # Clean the response text to remove markdown code block markers
        response_text = response_text.replace('```json', '').replace('```', '')
        response_text = response_text.strip()
        
        # Find JSON array in the response
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise Exception("No valid JSON array found in response")
            
        json_str = response_text[start_idx:end_idx]
        
        # Clean up the JSON string
        json_str = json_str.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        json_str = re.sub(r'\s+', ' ', json_str)  # Replace multiple spaces with single space
        
        # Remove any potential BOM or special characters at the start
        json_str = json_str.lstrip('\ufeff').lstrip()
        
        print("Cleaned JSON string (before final parse):", json_str)  # Debug print
        
        try:
            # First try to parse as is
            try:
                flashcards = json.loads(json_str)
            except json.JSONDecodeError:
                # If that fails, try to clean it further
                json_str = json_str.replace('\\n', ' ').replace('\\r', ' ').replace('\\t', ' ')
                json_str = re.sub(r'\\+', '\\', json_str)  # Fix any double escapes
                flashcards = json.loads(json_str)
            
            # Validate the structure of each flashcard
            for card in flashcards:
                if not all(key in card for key in ['question', 'answer', 'difficulty', 'topic']):
                    raise Exception("Invalid flashcard structure - missing required fields")
                if card['difficulty'] not in ['Easy', 'Medium', 'Hard']:
                    card['difficulty'] = 'Medium'  # Default to Medium if invalid
                # If section is required but missing, fill with 'General' or 'Unknown'
                if sections and 'section' not in card:
                    card['section'] = 'Unknown'
            
            return flashcards
            
        except json.JSONDecodeError as e:
            print("JSON parse error:", str(e))  # Debug print
            print("Attempted to parse:", json_str)  # Debug print
            raise Exception(f"Failed to parse JSON response: {str(e)}")

    except Exception as e:
        print("Gemini API error:", str(e))  # Debug print
        raise Exception(f"Gemini API error: {str(e)}")

@app.route('/api/translate', methods=['POST'])
def translate_text():
    try:
        data = request.json
        text = data.get('text')
        target_lang = data.get('targetLang')
        if not text or not target_lang:
            return jsonify({'error': 'Missing text or targetLang'}), 400
        url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={requests.utils.quote(text)}'
        resp = requests.get(url)
        if resp.status_code != 200:
            return jsonify({'error': 'Translation API error'}), 500
        data = resp.json()
        if isinstance(data, list) and isinstance(data[0], list) and isinstance(data[0][0], list):
            translated = data[0][0][0]
            return jsonify({'translated': translated})
        else:
            return jsonify({'error': 'Unexpected API response'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-answer', methods=['POST'])
def search_answer():
    try:
        data = request.json
        content = data.get('content')
        question = data.get('question')
        flashcards = data.get('flashcards', []) # Get flashcards, default to empty list if not present
        
        print("Search Answer received content length:", len(content) if content else 0) # Debug print
        print("Search Answer received question:", question) # Debug print
        print("Search Answer received flashcards count:", len(flashcards)) # Debug print

        if not content and not flashcards: # Modified check for content or flashcards
            return jsonify({'error': 'Missing content or flashcards to search in'}), 400
        if not question:
            return jsonify({'error': 'Missing question'}), 400

        # 1. Try to find answer directly in generated flashcards
        question_lower = question.lower()
        for card in flashcards:
            if question_lower in card.get('question', '').lower():
                return jsonify({'answer': card.get('answer', '')})
            if question_lower in card.get('answer', '').lower():
                return jsonify({'answer': card.get('answer', '')})

        # 2. If not found in flashcards, use Gemini model with original content
        if not content:
            return jsonify({'error': 'Sorry, the answer is not present in the provided content.'}), 200 # Or indicate no content for general search

        prompt = f"""
As an advanced AI assistant, your task is to precisely extract and provide the answer to the user's question SOLELY based on the following content.

Instructions:
1. If the answer is explicitly found in the content, provide it directly without any additional commentary or introductory phrases.
2. If the answer is NOT present in the content, respond with: "Sorry, the answer is not present in the provided content."
3. Do not invent information or use external knowledge.

Content:
{content}

Question: {question}

Answer:
"""
        model = genai.GenerativeModel('gemini-1.5-flash')
        generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 512,
        }
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        answer = response.text.strip()
        return jsonify({'answer': answer})
    except Exception as e:
        print("Error in search_answer:", str(e)) # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 