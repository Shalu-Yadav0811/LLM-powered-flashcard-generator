# LLM-Powered Flashcard Generator

A modern web application that generates interactive flashcards from educational content using Google Gemini AI. The app supports editing, translation, structure detection, and question search—all in a beautiful, user-friendly interface.

## Features

- **AI-Powered Flashcard Generation:**
  - Uses Google Gemini (via the gemini-1.5-flash model) to generate high-quality flashcards from pasted text or uploaded PDF content.
- **Difficulty Levels:**
  - Each flashcard is tagged as Easy, Medium, or Hard.
- **Edit Before Export:**
  - Edit any flashcard (question, answer, difficulty, topic) in a smooth modal before exporting.
- **Multi-language Support:**
  - Instantly translate all flashcards to multiple languages (Hindi, Spanish, French, etc.) using Google Translate (via backend proxy).
- **Structure Detection:**
  - Automatically detects and groups flashcards by chapters, subheadings, or sections in your content.
- **Question Search:**
  - Type any question and get an answer from your pasted text or PDF using Gemini (even if the answer is not in a flashcard).
- **Export Options:**
  - Export flashcards as JSON, CSV, Anki, or TXT.
- **Responsive UI:**
  - Works beautifully on desktop and mobile.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd <repo-directory>
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment:**
   - Create a `.env` file in the root directory and add your Google Gemini API key:
     ```
     GOOGLE_API_KEY=your_google_gemini_api_key_here
     FLASK_ENV=development
     ```

4. **Start the Flask backend:**
   ```bash
   python app.py
   ```

5. **Open the app:**
   - Visit [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

1. **Paste text or upload a PDF** to generate flashcards.
2. **Edit** any flashcard before exporting.
3. **Translate** flashcards to your preferred language.
4. **Search for answers** to your own questions from the content.
5. **Export** your flashcards in your desired format.

## Sample Execution

This section demonstrates a typical workflow using the provided sample PDF: `APznzaZUdlapAFWUKFjr-5SnuYRG6kF2yZKssJDVbSPfPu3DM0l4x72p_yOKHEvc_TN7aMtuLit-RwulHzqllkfWqbdvNB-VxVVmEbEEkLv9orKDSKz_voCV6lmoy1mxCY-BXkTHXsBdVlxssw9uYgF1Mj5nu7vDh3S67AAXU3zSMpQQRtp8FkK07u1bY-0B9GUyPwsmaEYLt.pdf`.

**1. Generating Flashcards from PDF Content:**

Upon uploading the PDF and clicking 'Generate Flashcards', the application processes the content and displays a set of flashcards. Due to the structure detection, flashcards are grouped by their respective sections (e.g., 'Introduction', 'Concepts', 'Algorithms').

*Example Flashcard (Front - Question):*
```
Card 1 - Binary Search Algorithm
What is Binary Search?
Click to reveal answer
```

*Example Flashcard (Back - Answer):*
```
Answer - Binary Search Algorithm
An efficient algorithm for finding an item from a sorted list of elements by repeatedly dividing the search interval in half.
Click to see question
```

**2. Translating Flashcards:**

After generation, you can select a language (e.g., Hindi) from the dropdown and click 'Translate'. The flashcards will be instantly translated.

*Example Translated Flashcard (Hindi):*
```
कार्ड 1 - बाइनरी सर्च एल्गोरिथम
बाइनरी सर्च क्या है?
उत्तर प्रकट करने के लिए क्लिक करें
```

**3. Searching for an Answer:**

You can also search for specific answers within the content. For instance, if you type "What is the key requirement for Binary Search?" into the search bar, you would get an answer directly from the content.

*Example Search Result:* 
```
Answer
The input list or array must be sorted.
```

## Screenshots

*(Add your screenshots here to visually demonstrate the features)* 

### 1. Search for an Answer with Error

![Search for an Answer with Error](Screenshot%202025-06-13%20155408.png)

### 2. Search Result and Flashcard Example

![Search Result and Flashcard Example](Screenshot%202025-06-13%20155343.png)

### 3. Flashcard View

![Flashcard View](Screenshot%202025-06-13%20155238.png) 