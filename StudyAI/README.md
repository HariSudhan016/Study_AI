# StudyAI

**StudyAI** is an AI-powered academic assistant that uses Retrieval-Augmented Generation to help students interact with their study materials. Students can upload PDFs, ask context-aware questions, generate summaries and quizzes, simplify difficult concepts, and prepare structured examination answers. The system combines local semantic search using Sentence Transformers and FAISS with Google's Gemini generative AI model.

---

## Features

1. **PDF Question Answering (Chat)**: Ask questions directly and receive grounded, accurate answers backed by your notes.
2. **Retrieval-Augmented Generation (RAG)**: Automatically searches and retrieves only the most relevant pages/sections from your notes to construct answers.
3. **Source References**: See exactly where information comes from (source document and page numbers).
4. **AI Notes Summarization**: Summarize entire textbooks or slides into high-yield, exam-focused chapters.
5. **Beginner-Friendly Concept Explanations**: Convert dense academic jargon into simple definitions, real-world analogies, and examples.
6. **Interactive MCQ Practice Quizzes**: Generate and take custom multiple-choice quizzes with immediate grading and detailed explanations.
7. **Important Exam Questions**: Generate predicted exam questions grouped by short (2-mark), medium (5-mark), and long (13/14-mark) layouts.
8. **University-Style Essay Answer Writer**: Formulate comprehensive 13/14-mark answers structured into standard academic headings including definition, diagram, practical example, advantages, applications, and conclusion.

---

## Tech Stack

* **Frontend**: Streamlit
* **PDF Processing**: PyPDF
* **Embeddings**: Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2` running locally)
* **Vector Index**: FAISS (in-memory CPU index)
* **LLM Model**: Google Gemini API (`gemini-1.5-flash`)
* **Language**: Python 3.10+

---

## System Architecture

```
                                      +------------------+
                                      |   Study PDF(s)   |
                                      +--------+---------+
                                               |
                                               v (PyPDF Page Extraction)
                                      +--------+---------+
                                      |   Text Cleaned   |
                                      +--------+---------+
                                               |
                                               v (Sliding-Window Chunking)
                                      +--------+---------+
                                      |   Text Chunks    |
                                      +--------+---------+
                                               |
                                               v (Local Sentence Transformer)
                                      +--------+---------+
                                      | Embeddings (384d)|
                                      +--------+---------+
                                               |
                                               v
+------------------+          +--------+---------+
|  User Question   |          |  FAISS CPU Index |
+--------+---------+          +--------+---------+
         |                             ^
         v (Embed query)               |
+--------+---------+                   | (Retrieve Top k Chunks)
| Query Embedding  +-------------------+
+--------+---------+
         |
         v
+--------+---------+          +------------------+
| Grounded Prompt  +--------->|    Gemini API    |
+------------------+          +--------+---------+
                                       |
                                       v (Generate response)
                              +--------+---------+
                              | Streamlit Chat   |
                              +------------------+
```

---

## Installation

Follow these steps to set up and run the application on your computer:

### 1. Clone or Open the Workspace
Ensure you are in the project folder `StudyAI`:
```bash
cd c:\Users\Navamanikandan\OneDrive\Desktop\StudyAI
```

### 2. Set Up a Virtual Environment (Recommended)
Create and activate a python virtual environment to isolate dependencies:
```bash
# On Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all required libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## Google Gemini API Key Setup

StudyAI uses the Gemini API to answer questions and generate study aids.

1. Get a free API key from the [Google AI Studio](https://aistudio.google.com/).
2. Create or edit the file `.streamlit/secrets.toml` in the project root:
   ```toml
   GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
   ```
3. **Important Security Warning**: Never commit your actual API key to GitHub. The project's `.gitignore` is pre-configured to ignore `.streamlit/secrets.toml`.

---

## Running the Application

To launch the Streamlit server and run the application locally:

```bash
streamlit run app.py
```

Once running, the application will automatically open in your default web browser at `http://localhost:8501`.
