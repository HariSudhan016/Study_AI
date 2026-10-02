import streamlit as st
import os
import numpy as np

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="StudyAI — AI Academic Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern SaaS Design System (Custom CSS Injection)
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    /* Hide Streamlit default header decoration for clean app feeling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Custom Container Cards */
    .saas-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.2);
    }
    .saas-card:hover {
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.12);
        transform: translateY(-2px);
    }

    /* Icon Box */
    .icon-box {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.35rem;
        margin-bottom: 1rem;
    }

    /* Hero Section */
    .hero-container {
        padding: 2.5rem 2rem;
        background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.05) 50%, transparent 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94A3B8;
        max-width: 650px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 1.1rem;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #A5B4FC;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1.25rem;
    }

    /* Status Pills */
    .status-pill-active {
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }
    .status-pill-idle {
        background: rgba(245, 158, 11, 0.12);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Sidebar Logo Header */
    .sidebar-logo-container {
        padding: 0.5rem 0.2rem 1.25rem 0.2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1.5rem;
    }
    .sidebar-brand-name {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #818CF8 0%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sidebar-brand-tagline {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 500;
    }

    /* Document Status Panel in Sidebar */
    .sidebar-status-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Feature Titles & Descriptions */
    .feature-card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.4rem;
    }
    .feature-card-desc {
        font-size: 0.88rem;
        color: #94A3B8;
        line-height: 1.5;
    }

    /* Callout Card (Explain Simply / Quiz) */
    .callout-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Imports from project modules
from pdf_processor import extract_text_from_pdf, chunk_text
from rag import load_embedding_model, build_faiss_index, search_faiss_index
import ai

# Initialize Session State
if "processed_files" not in st.session_state:
    st.session_state.processed_files = {}  # filename -> list of chunks
if "all_chunks" not in st.session_state:
    st.session_state.all_chunks = []
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_quiz" not in st.session_state:
    st.session_state.active_quiz = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_graded" not in st.session_state:
    st.session_state.quiz_graded = False

# Load local embedding model (cached via Streamlit)
with st.spinner("Initializing local embedding model (sentence-transformers)... Please wait..."):
    try:
        embedding_model = load_embedding_model()
    except Exception as e:
        st.error(f"Error loading embedding model: {e}")
        st.stop()

# Helper function to check if any study material is uploaded
def check_material_uploaded():
    if not st.session_state.processed_files:
        st.warning("⚠️ Please upload and process study material PDF(s) in the **📚 Study Material** section first.")
        st.stop()

# Sidebar Brand Header
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo-container">
        <div class="sidebar-brand-name">🎓 StudyAI</div>
        <div class="sidebar-brand-tagline">AI-Powered Academic Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Document Index Status Badge in Sidebar
    if st.session_state.processed_files:
        file_count = len(st.session_state.processed_files)
        chunk_count = len(st.session_state.all_chunks)
        st.markdown(f"""
        <div class="sidebar-status-box">
            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 0.3rem;">INDEX STATUS</div>
            <div class="status-pill-active">🟢 RAG Active ({file_count} PDF{'s' if file_count > 1 else ''})</div>
            <div style="font-size: 0.78rem; color: #64748B; margin-top: 0.5rem;">{chunk_count} indexed text segments ready</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sidebar-status-box">
            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 0.3rem;">INDEX STATUS</div>
            <div class="status-pill-idle">🟡 Awaiting PDF Upload</div>
            <div style="font-size: 0.78rem; color: #64748B; margin-top: 0.5rem;">No documents in memory</div>
        </div>
        """, unsafe_allow_html=True)

# Navigation Menu
navigation = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Home Dashboard",
        "📚 Study Material",
        "💬 Ask AI (Chat)",
        "📄 Summary Notes",
        "🧠 Explain Simply",
        "📝 Interactive Quiz",
        "❓ Exam Questions",
        "✍️ 13/14-Mark Answer"
    ]
)

# ----------------- HOME DASHBOARD -----------------
if navigation == "🏠 Home Dashboard":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">⚡ RAG-Powered AI Learning Workspace</div>
        <h1 class="hero-title">Study Smarter with StudyAI</h1>
        <div class="hero-subtitle">
            Upload your university notes, textbooks, or slides. StudyAI builds a local vector index to deliver context-grounded Q&A, exam preparations, revision summaries, and quizzes.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-Time Session Metrics Panel
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Loaded PDFs", value=len(st.session_state.processed_files))
    with m2:
        total_pages = sum(d["pages"] for d in st.session_state.processed_files.values()) if st.session_state.processed_files else 0
        st.metric(label="Total Pages Indexed", value=total_pages)
    with m3:
        st.metric(label="Vector Text Segments", value=len(st.session_state.all_chunks))
    with m4:
        st.metric(label="Conversations", value=len([m for m in st.session_state.chat_history if m["role"] == "user"]))
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Core Assistant Modules")
    
    # Showcase Feature Cards in a 3x2 Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="saas-card">
            <div class="icon-box">📚</div>
            <div class="feature-card-title">Document Manager</div>
            <div class="feature-card-desc">Upload course materials, slide decks, and past papers for page-by-page semantic text indexing.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="saas-card">
            <div class="icon-box">🧠</div>
            <div class="feature-card-title">Explain Simply</div>
            <div class="feature-card-desc">Translate complex definitions into beginner analogies, technical terms, and real-world examples.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="saas-card">
            <div class="icon-box">💬</div>
            <div class="feature-card-title">Grounded Q&A Chat</div>
            <div class="feature-card-desc">Ask questions about your uploaded materials. Get exact answers complete with source page references.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="saas-card">
            <div class="icon-box">📝</div>
            <div class="feature-card-title">Interactive Quizzes</div>
            <div class="feature-card-desc">Generate multiple-choice practice tests with instant scoring, feedback, and concept explanations.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="saas-card">
            <div class="icon-box">📄</div>
            <div class="feature-card-title">Revision Summaries</div>
            <div class="feature-card-desc">Synthesize entire chapters into structured main concepts, key definitions, and quick revision sheets.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="saas-card">
            <div class="icon-box">✍️</div>
            <div class="feature-card-title">University Exam Answers</div>
            <div class="feature-card-desc">Generate 13/14-mark structured essay responses structured with definitions, diagrams, and applications.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Status Callout
    if not st.session_state.processed_files:
        st.info("💡 **Get Started**: Click **📚 Study Material** in the sidebar to upload your first study PDF.")
    else:
        st.success("✅ **Ready to Assist**: Your materials are loaded! Navigate to **💬 Ask AI (Chat)** or any study module to begin.")

# ----------------- STUDY MATERIAL (UPLOAD) -----------------
elif navigation == "📚 Study Material":
    st.title("📚 Study Material Manager")
    st.write("Upload university study documents (PDF format). The text is extracted, chunked, and indexed locally on your system.")
    
    # Clean Container for File Uploader
    with st.container():
        uploaded_files = st.file_uploader(
            "Select one or more PDF study files",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload PDF textbooks, lecture slides, or revision notes."
        )
        
    if uploaded_files:
        new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
        
        if new_files:
            for f in new_files:
                with st.spinner(f"Processing '{f.name}'..."):
                    # Extract page-by-page text
                    pages_data = extract_text_from_pdf(f)
                    
                    if not pages_data:
                        st.error(f"Could not extract any text from '{f.name}'. Is it an empty or scanned image-only PDF?")
                        continue
                        
                    # Chunk pages
                    chunks = chunk_text(pages_data)
                    
                    # Store chunks associated with file
                    st.session_state.processed_files[f.name] = {
                        "pages": len(pages_data),
                        "chunks": chunks
                    }
                    
            # Recompile all chunks and rebuild the FAISS vector index
            all_chunks = []
            for filename, data in st.session_state.processed_files.items():
                all_chunks.extend(data["chunks"])
                
            st.session_state.all_chunks = all_chunks
            
            with st.spinner("Building FAISS semantic search index..."):
                st.session_state.faiss_index = build_faiss_index(all_chunks, embedding_model)
                
            st.success("✅ Study materials updated and indexed successfully!")
            
    # Display Active Inventory Cards
    if st.session_state.processed_files:
        st.markdown("---")
        st.markdown("### Loaded Documents")
        
        for filename, data in st.session_state.processed_files.items():
            with st.container():
                st.markdown(f"""
                <div class="saas-card" style="padding: 1rem 1.25rem; margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC;">📄 {filename}</div>
                        <div style="display: flex; gap: 0.75rem;">
                            <span class="status-pill-active">📖 {data['pages']} Pages</span>
                            <span class="status-pill-active">🧩 {len(data['chunks'])} Chunks</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear All Loaded Materials", type="primary"):
            st.session_state.processed_files = {}
            st.session_state.all_chunks = []
            st.session_state.faiss_index = None
            st.session_state.chat_history = []
            st.session_state.active_quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_graded = False
            st.success("All study materials cleared from memory.")
            st.rerun()
    else:
        st.info("No files uploaded. Drag and drop PDF files into the uploader above to begin.")

# ----------------- ASK AI (CHAT WITH REFERENCES) -----------------
elif navigation == "💬 Ask AI (Chat)":
    st.title("💬 Chat with StudyAI")
    check_material_uploaded()
    
    st.write("Ask questions about your uploaded study materials. StudyAI will retrieve the most relevant sections of your documents to ground its answer.")
    
    # Top Action Bar
    c_left, c_right = st.columns([4, 1])
    with c_right:
        if st.button("🧹 Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history reset.")
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render past chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("🔍 Verified Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"- **{src['source']}** — Page {src['page']} *(relevance score: {src['score']:.2f})*")
                        
    # Input box for new query
    if user_query := st.chat_input("Ask a question based on your study material..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)
            
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Retrieval Phase
        with st.spinner("Searching document vector index..."):
            retrieved = search_faiss_index(user_query, st.session_state.faiss_index, st.session_state.all_chunks, embedding_model, k=4)
            
        # Generation Phase
        with st.chat_message("assistant"):
            if not retrieved:
                ans_text = "I couldn't retrieve any relevant information. Please ensure you have uploaded documents."
                st.markdown(ans_text)
                st.session_state.chat_history.append({"role": "assistant", "content": ans_text, "sources": []})
            else:
                message_placeholder = st.empty()
                with st.spinner("Consulting Gemini..."):
                    try:
                        ans_text = ai.generate_grounded_answer(user_query, retrieved)
                        message_placeholder.markdown(ans_text)
                        
                        # Show sources under expander
                        with st.expander("🔍 Verified Sources"):
                            for src in retrieved:
                                st.markdown(f"- **{src['source']}** — Page {src['page']} *(relevance score: {src['score']:.2f})*")
                        
                        # Save to history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": ans_text,
                            "sources": retrieved
                        })
                    except Exception as e:
                        message_placeholder.error(f"Failed to generate answer: {e}")

# ----------------- SUMMARIZE NOTES -----------------
elif navigation == "📄 Summary Notes":
    st.title("📄 Generate Summarized Notes")
    check_material_uploaded()
    
    st.write("Generate a structured revision summary of the loaded notes. StudyAI samples key segments from across the material to draft a high-yield study sheet.")
    
    if st.button("⚡ Generate Chapter Summary", type="primary"):
        # Select representative chunks evenly across the documents to summarize the entire text
        total = len(st.session_state.all_chunks)
        if total <= 40:
            summary_chunks = st.session_state.all_chunks
        else:
            step = total // 40
            summary_chunks = st.session_state.all_chunks[::step][:40]
            
        with st.spinner("Analyzing study material and writing summary..."):
            try:
                summary_md = ai.generate_summary(summary_chunks)
                st.markdown("---")
                st.markdown(summary_md)
                
                # Option to download summary as markdown
                st.download_button(
                    label="📥 Download Summary (.md)",
                    data=summary_md,
                    file_name="StudyAI_Summary.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Error generating summary: {e}")

# ----------------- EXPLAIN SIMPLY -----------------
elif navigation == "🧠 Explain Simply":
    st.title("🧠 Explain Simply (Beginner Mode)")
    check_material_uploaded()
    
    st.write("Convert complicated concepts or jargon into simple language, analogies, and practical examples.")
    
    concept = st.text_input("What concept would you like to simplify?", placeholder="e.g. Deadlock, OSI Layer 4, Pointers, Dijkstra's algorithm")
    
    if st.button("💡 Simplify It", type="primary"):
        if not concept.strip():
            st.warning("Please enter a concept name.")
        else:
            # Semantic search to retrieve chunks related to the concept
            with st.spinner(f"Retrieving context for '{concept}'..."):
                retrieved = search_faiss_index(concept, st.session_state.faiss_index, st.session_state.all_chunks, embedding_model, k=4)
                
            with st.spinner("Generating simple explanation..."):
                try:
                    simplified_explanation = ai.explain_simply(concept, retrieved)
                    st.markdown("---")
                    st.markdown(simplified_explanation)
                except Exception as e:
                    st.error(f"Error simplifying concept: {e}")

# ----------------- INTERACTIVE MCQ QUIZ -----------------
elif navigation == "📝 Interactive Quiz":
    st.title("📝 MCQ Practice Quiz")
    check_material_uploaded()
    
    st.write("Test your knowledge! Generate educational multiple-choice questions grounded in your loaded materials.")
    
    # Quiz Configuration Form
    if st.session_state.active_quiz is None:
        q_count = st.selectbox("Select number of questions:", [5, 10, 15], index=0)
        if st.button("🎲 Generate Quiz", type="primary"):
            # Sample chunks for generating the quiz
            total = len(st.session_state.all_chunks)
            if total <= 25:
                quiz_chunks = st.session_state.all_chunks
            else:
                step = total // 25
                quiz_chunks = st.session_state.all_chunks[::step][:25]
                
            with st.spinner("Drafting educational quiz questions..."):
                try:
                    quiz_list = ai.generate_mcq_quiz(quiz_chunks, q_count)
                    st.session_state.active_quiz = quiz_list
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_graded = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to generate quiz: {e}")
    else:
        # Display the active quiz
        st.success(f"Generated a {len(st.session_state.active_quiz)}-question quiz based on your materials.")
        
        # Display questions
        for idx, item in enumerate(st.session_state.active_quiz):
            st.markdown(f"**Question {idx + 1}: {item['question']}**")
            
            # Map index option to key
            options = item["options"]
            
            # Use state to persist answers
            saved_ans = st.session_state.quiz_answers.get(idx, None)
            
            # Determine selected option index
            choice_idx = None
            if saved_ans in ["A", "B", "C", "D"]:
                choice_idx = ["A", "B", "C", "D"].index(saved_ans)
                
            selected_option = st.radio(
                f"Choose option for Q{idx+1}:",
                options,
                index=choice_idx,
                key=f"q_{idx}",
                label_visibility="collapsed"
            )
            
            # Save selection to state
            if selected_option:
                opt_letter = ["A", "B", "C", "D"][options.index(selected_option)]
                st.session_state.quiz_answers[idx] = opt_letter
                
            # If graded, show answer evaluation
            if st.session_state.quiz_graded:
                user_letter = st.session_state.quiz_answers.get(idx, "None")
                correct_letter = item["answer"]
                
                if user_letter == correct_letter:
                    st.success(f"✅ **Correct!** Answer: {correct_letter}")
                else:
                    st.error(f"❌ **Incorrect.** You selected {user_letter}. Correct Answer: {correct_letter}")
                    
                st.info(f"💡 **Explanation**: {item['explanation']}")
            st.markdown("---")
            
        # Grade/Reset Buttons
        if not st.session_state.quiz_graded:
            if st.button("💯 Grade My Answers", type="primary"):
                st.session_state.quiz_graded = True
                st.rerun()
        else:
            # Show score
            score = 0
            for idx, item in enumerate(st.session_state.active_quiz):
                if st.session_state.quiz_answers.get(idx, "") == item["answer"]:
                    score += 1
            st.balloons()
            st.metric("Your Score", f"{score} / {len(st.session_state.active_quiz)}", f"{int(score/len(st.session_state.active_quiz)*100)}%")
            
            if st.button("🔄 Generate A New Quiz"):
                st.session_state.active_quiz = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_graded = False
                st.rerun()

# ----------------- IMPORTANT EXAM QUESTIONS -----------------
elif navigation == "❓ Exam Questions":
    st.title("❓ Likely Exam Questions")
    check_material_uploaded()
    
    st.write("StudyAI analyzes your notes to identify high-yield exam questions, categorized by their typical university mark scheme weight.")
    
    if st.button("🎯 Predict Exam Questions", type="primary"):
        total = len(st.session_state.all_chunks)
        if total <= 30:
            exam_chunks = st.session_state.all_chunks
        else:
            step = total // 30
            exam_chunks = st.session_state.all_chunks[::step][:30]
            
        with st.spinner("Analyzing text patterns for exam topics..."):
            try:
                questions_md = ai.generate_exam_questions(exam_chunks)
                st.markdown("---")
                st.markdown(questions_md)
            except Exception as e:
                st.error(f"Error generating exam questions: {e}")

# ----------------- 13/14-MARK ANSWER GENERATOR -----------------
elif navigation == "✍️ 13/14-Mark Answer":
    st.title("✍️ University 13/14-Mark Answer Writer")
    check_material_uploaded()
    
    st.write("Generate a comprehensive, fully structured essay-style answer for university examinations. The output adheres to a strict academic outline including introduction, formal definitions, detailed explanations, diagrams, examples, advantages, and applications.")
    
    exam_question = st.text_input("Enter the exam question:", placeholder="e.g. Describe the architecture of OSI Reference Model in detail.")
    
    if st.button("✍️ Write Comprehensive Answer", type="primary"):
        if not exam_question.strip():
            st.warning("Please enter a question to answer.")
        else:
            # Semantic search to retrieve chunks related to the question
            with st.spinner("Finding relevant study materials..."):
                retrieved = search_faiss_index(exam_question, st.session_state.faiss_index, st.session_state.all_chunks, embedding_model, k=8)
                
            with st.spinner("Drafting structured academic answer..."):
                try:
                    structured_ans = ai.generate_long_answer(exam_question, retrieved)
                    st.markdown("---")
                    st.markdown(structured_ans)
                    
                    # Option to download answer
                    st.download_button(
                        label="📥 Download Answer (.md)",
                        data=structured_ans,
                        file_name="Exam_Answer.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Error generating answer: {e}")
