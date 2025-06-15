# 🧠 LLM-Powered Flashcard Generator

A modern web application that generates interactive, multilingual flashcards from educational content using **Google Gemini AI**. Built for students, educators, and professionals, the tool offers a sleek interface, AI question-answer generation, content structuring, live search, and multiple export formats.

---

## 🚀 Features

### 🤖 AI-Powered Flashcard Generation
- Uses **Google Gemini (gemini-1.5-flash)** to generate high-quality flashcards from **pasted text** or **PDF uploads**.

### 📊 Difficulty Levels
- Each flashcard is labeled **Easy**, **Medium**, or **Hard** to help tailor study sessions.

### ✍️ In-App Flashcard Editing
- Edit questions, answers, topics, and difficulty levels in a user-friendly **modal editor** before exporting.

### 🌐 Multi-language Support
- Translate flashcards into **Hindi, Spanish, French, and more** using **Google Translate API (via backend proxy)**.

### 🧩 Structure Detection
- Automatically detects **chapters, subheadings, and sections** to group flashcards logically.

### 🔍 Intelligent Question Search
- Type any question and retrieve accurate answers using Gemini—even if not explicitly in the flashcards.

### 📤 Multiple Export Options
- Export your flashcards to **JSON**, **CSV**, **Anki (.apkg)**, or **plain TXT**.

### 📱 Responsive UI
- Fully responsive interface—**mobile and desktop friendly**.

---

## 🧰 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-github-repo-url>
cd <repo-directory>
```
### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a .env file in the root directory and add:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
FLASK_ENV=development
```

### 4. Start the Flask Backend

```bash
python app.py
```

### 5. Open the App in Your Browser

```bash
http://localhost:5000
```

## 🧪 Usage Guide

- Upload a **PDF** or paste **raw text**.
- Click **Generate Flashcards** to begin AI processing.
- Edit individual flashcards as needed.
- Use the **language dropdown** to translate flashcards.
- Enter any **custom question** to get answers via Gemini AI.
- Export your final set in your desired format (JSON, CSV, Anki, TXT).

## Sample Execution
This section demonstrates a typical workflow using the provided sample PDF: APznzaZUdlapAFWUKFjr-5SnuYRG6kF2yZKssJDVbSPfPu3DM0l4x72p_yOKHEvc_TN7aMtuLit-RwulHzqllkfWqbdvNB-VxVVmEbEEkLv9orKDSKz_voCV6lmoy1mxCY-BXkTHXsBdVlxssw9uYgF1Mj5nu7vDh3S67AAXU3zSMpQQRtp8FkK07u1bY-0B9GUyPwsmaEYLt.pdf.

1. Generating Flashcards from PDF Content:

Upload a document related to Computer Networks and click "Generate Flashcards". The app processes the content using Gemini and creates flashcards grouped by topic (e.g., OSI Model, IP Addressing, Routing Protocols).

Example Flashcard (Front - Question):

Q: What is the purpose of the OSI model?
A: It standardizes networking functions into seven layers to ensure interoperability between systems.

2. Translating Flashcards:

Q: What is the difference between TCP and UDP?
A: TCP is connection-oriented and reliable, while UDP is faster but connectionless and less reliable.

Example Translated Flashcard (Hindi):

Q: OSI मॉडल का उद्देश्य क्या है?
A: यह नेटवर्किंग कार्यों को सात परतों में विभाजित करता है जिससे विभिन्न प्रणालियों के बीच पारस्परिक क्रियाशीलता सुनिश्चित होती है।

3. Searching for an Answer:

You can also search for specific answers within the uploaded content. For instance, if you type "Why is the OSI model important?" into the search bar, you’ll get a direct and accurate answer based on the document's content.

Example Search Result:

Answer
The OSI model is important because it standardizes the functions of a telecommunication or computing system into seven distinct layers, enabling interoperability among different systems and protocols.

## Screenshots

### 1. Search for an Answer with Error
![Screenshot 2025-06-15 155416](https://github.com/user-attachments/assets/c8258b69-8d15-443f-9f99-d18eb4c4bdfc)

### 2. Search Result and Flashcard Example
![Screenshot 2025-06-15 155338](https://github.com/user-attachments/assets/85d62aad-6bbd-495a-b0de-7b580f02e9dc)

### 3. Flashcard View
![Screenshot 2025-06-15 155303](https://github.com/user-attachments/assets/9d69771e-921f-43ef-a649-a0ba685260fa)

## 🧭 Roadmap / To-Do

- [ ] Flashcard review mode  
- [ ] Flashcard shuffling  
- [ ] Dark mode  
- [ ] Subject-wise export  
- [ ] Flashcard tagging system

## ✨ Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [Flask](https://flask.palletsprojects.com/)
- [Google Translate API](https://cloud.google.com/translate)

## 💬 Feedback

- Found a bug or want to suggest a feature?  
- Feel free to [open an issue](https://github.com/Shalu-Yadav0811/LLM-powered-flashcard-generator/issues) or submit a pull request.  
Contributions are welcome and appreciated!
