# 🎓 StudyAI

### 📚 AI-Powered Study Assistant for College Students

StudyAI is an AI-powered study assistant designed to help students learn from their study materials more effectively.

Users can upload PDF study materials and interact with them using AI-powered question answering, document search, summaries, and learning assistance.

---

## 🚀 Live Demo

🌐 *Try StudyAI Online:*

👉 [Open StudyAI](https://studyai-bowbwkrqg22icy5o2yvkk8.streamlit.app/)

---

## 📌 About the Project

Studying from large PDF documents can be time-consuming, especially when students need to quickly find specific information or understand difficult topics.

*StudyAI* solves this problem by allowing students to upload their study materials and ask questions directly about the content.

The application uses a *Retrieval-Augmented Generation (RAG)* approach to retrieve relevant information from uploaded documents and provide AI-generated responses based on that context.

---

## ✨ Features

### 📄 PDF Study Material Upload
Upload your college notes, textbooks, lecture materials, or other PDF documents.

### 🤖 AI Question Answering
Ask questions about the uploaded study material and receive AI-generated answers.

### 🔍 Intelligent Document Search
StudyAI searches through the uploaded document and retrieves the most relevant information.

### 🧠 Retrieval-Augmented Generation
The application combines document retrieval with generative AI to provide context-aware answers.

### 📝 Study Summaries
Generate concise summaries from study materials to make revision easier.

### ❓ Practice Questions
Generate questions from your study material for exam preparation.

### 🎓 Student-Focused
Designed specifically to make studying and revision easier for college students.

### ☁️ Web Deployment
The application is deployed using Streamlit and can be accessed through a web browser.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🎈 Streamlit | Web application framework |
| 🤖 Google Gemini | AI-powered responses |
| 🧠 Sentence Transformers | Text embeddings |
| 🔎 FAISS | Similarity search |
| 📄 PyPDF | PDF text extraction |
| 🔗 RAG | Document-based AI question answering |

---

## 🏗️ How StudyAI Works

```text
                ┌─────────────────────┐
                │     PDF Upload      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   PDF Text          │
                │   Extraction        │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Text Processing &   │
                │ Chunking            │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Sentence            │
                │ Transformer Model   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ FAISS Vector        │
                │ Database            │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Relevant Context    │
                │ Retrieval           │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Google Gemini       │
                │ AI Model            │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ AI Generated        │
                │ Response            │
                └─────────────────────┘

📂 Project Structure
StudyAI/
│
├── .streamlit/
│   └── config.toml
│
├── ai.py
├── app.py
├── pdf_processor.py
├── rag.py
│
├── README.md
├── requirements.txt
└── .gitignore
📄 File Description
File	Description
app.py	Main Streamlit application
ai.py	AI/Gemini functionality
pdf_processor.py	PDF text extraction and processing
rag.py	RAG pipeline and document retrieval
requirements.txt	Python dependencies
.gitignore	Files excluded from Git
README.md	Project documentation
.streamlit/config.toml	Streamlit configuration
⚙️ Installation
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/StudyAI.git
2. Navigate to the Project
cd StudyAI
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
5. Install Dependencies
pip install -r requirements.txt
🔐 API Key Configuration

StudyAI uses the Google Gemini API for AI-powered responses.

Create the following file:

.streamlit/secrets.toml

Add your API key:

GEMINI_API_KEY = "YOUR_API_KEY"
⚠️ Important

Never upload your API key to GitHub.

The secrets.toml file is excluded from Git using .gitignore.

Example:

.streamlit/secrets.toml
▶️ Run the Application Locally

After installing all dependencies, run:

streamlit run app.py

The application will open in your browser.

Usually, Streamlit will run at:

http://localhost:8501
☁️ Deployment

StudyAI is deployed using Streamlit Community Cloud.

🌐 Live Application

👉 Launch StudyAI

The application can be accessed directly through a web browser without installing the project locally.

🎯 Use Cases

StudyAI can be used for:

🎓 College exam preparation
📚 Understanding lecture notes
📖 Studying textbooks
📝 Revision
🔍 Searching large PDF documents
❓ Generating practice questions
🧠 Understanding difficult topics
📑 Summarizing study materials
🎯 Quick preparation before exams
💡 Example Workflow
1. Open StudyAI
        ↓
2. Upload your PDF
        ↓
3. StudyAI processes the document
        ↓
4. Ask a question
        ↓
5. Relevant content is retrieved
        ↓
6. AI generates an answer
        ↓
7. Use the response for learning and revision
🔮 Future Improvements

The project can be extended with several additional features:

🎤 Voice-based interaction
🌐 Multi-language support
🇮🇳 Tamil language support
📊 Student learning analytics
🗂️ Multiple PDF conversations
📝 Advanced quiz generation
📑 Automatic note generation
📈 Personalized study plans
📱 Improved mobile interface
💬 Conversation history
🔖 Bookmark important answers
📚 Multiple-document question answering
🎯 Personalized exam preparation
🔒 Security

StudyAI follows basic security practices for handling API credentials.

Sensitive files such as:

.streamlit/secrets.toml
.env

are excluded from the Git repository.

Never commit API keys, passwords, or other private credentials to GitHub.

🧪 Project Status

Status: ✅ Working

StudyAI is currently deployed and available as a web application.

🚀 Live Demo: Open StudyAI

👨‍💻 Developer
Navamani Kandan

B.Tech CSE (AI & ML) Student

Interested in:

Artificial Intelligence
Machine Learning
Software Development
Python
Java
Data Structures & Algorithms
🔗 Profiles
💻 GitHub: Navamani5251
🧩 LeetCode: Navamanikandan
⭐ Support

If you find StudyAI useful, consider giving this repository a ⭐ on GitHub.

Your support helps motivate further development of the project!

📜 License

This project is available under the MIT License.

🎓 StudyAI
Learn smarter. Search faster. Study better.

🚀 Try StudyAI Live


### One small thing before you push

Your GitHub repo will look much better if you also add a **screenshot of the StudyAI UI** near the top of the README. For example:

```markdown
## 🖥️ Preview

![StudyAI Preview](assets/studyai-preview.png)
