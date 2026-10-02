from google import genai
from google.genai import types
import streamlit as st
import json

def get_gemini_client():
    """
    Configures and retrieves the Google GenAI Client instance.
    Raises ValueError if the API key is missing or is the default placeholder.
    """
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        raise ValueError(
            "Gemini API key is not configured.\n\n"
            "Please follow these steps to add it:\n"
            "1. Open the file `.streamlit/secrets.toml` in the project directory.\n"
            "2. Replace `'YOUR_GEMINI_API_KEY_HERE'` with your actual Google Gemini API key.\n"
            "3. Restart the Streamlit app."
        )
        
    # Initialize the official Google GenAI Client
    return genai.Client(api_key=api_key)

def get_system_instruction() -> str:
    """
    Returns the core system prompt rules for StudyAI.
    """
    return (
        "You are StudyAI, an intelligent academic assistant for college students.\n"
        "Your primary source of truth is the student's uploaded study material.\n\n"
        "Rules:\n"
        "1. Use the provided study material whenever possible.\n"
        "2. Do not invent information.\n"
        "3. If the answer is not available in the uploaded material, clearly state that.\n"
        "4. Explain concepts in simple student-friendly language.\n"
        "5. Use examples when useful.\n"
        "6. Structure answers clearly.\n"
        "7. Highlight important examination points.\n"
        "8. When generating exam answers, use appropriate academic structure.\n"
        "9. Do not unnecessarily repeat information.\n"
        "10. Do not claim certainty when the source material does not support the answer."
    )

def generate_grounded_answer(question: str, context_chunks: list) -> str:
    """
    Generates a Q&A response grounded in retrieved PDF context.
    """
    client = get_gemini_client()
    
    # Build context string
    context_str = ""
    for i, chunk in enumerate(context_chunks):
        context_str += f"\n--- Context Section {i+1} (Source: {chunk['source']}, Page: {chunk['page']}) ---\n"
        context_str += chunk["text"] + "\n"
        
    prompt = f"""
Context from student's study material:
{context_str}

Question: {question}

Instructions:
Answer the student's question based strictly on the provided context sections above.
If the context does not contain the answer, clearly state: "I couldn't find the answer to this question in your uploaded study material." and do not try to invent an answer.

Ensure your response is structured with:
1. A **Simple Explanation** of the concept in conversational, student-friendly language.
2. **Important Points** (bullet points highlighting key mechanics or facts).
3. A concrete **Example**.
4. An **Exam-friendly Explanation** or exam tips (where appropriate).

Format the response clearly using markdown headings, bold text, and bullet points.
"""
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction()
        )
    )
    return response.text

def explain_simply(concept: str, context_chunks: list) -> str:
    """
    Simplifies a difficult concept using definitions, analogies, and code/practical examples.
    """
    client = get_gemini_client()
    
    context_str = ""
    for i, chunk in enumerate(context_chunks):
        context_str += f"\n--- Section {i+1} ---\n{chunk['text']}\n"
        
    prompt = f"""
Context from student's study material:
{context_str}

Concept to explain: {concept}

Instructions:
Explain this concept in extremely simple, beginner-friendly terms using the provided context material.
If the concept is not mentioned in the context material, you can use your general knowledge, but first explicitly state:
"*(Note: This concept was not found in your study material, but here is a simple explanation based on general academic knowledge)*"

Structure your response into these exact sections with markdown headings:
1. ### 💡 Simple Definition
   (Explain the concept in 1-2 sentences using absolutely no technical jargon, as if explaining to a 10-year-old).
2. ### 🎨 Real-World Analogy
   (Provide a relatable, vivid real-world analogy to illustrate the concept).
3. ### ⚙️ Technical Explanation
   (Provide a brief, clear technical explanation for a college student, defining key terms simply).
4. ### 💻 Practical Example
   (Show a concrete example, scenario, or walkthrough where this is applied).

Avoid unnecessarily complicated terminology.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction()
        )
    )
    return response.text

def generate_summary(context_chunks: list) -> str:
    """
    Summarizes all chunks of the study material in an exam-focused structure.
    """
    client = get_gemini_client()
    
    context_str = ""
    for chunk in context_chunks:
        context_str += f"\n[Page {chunk['page']}]\n{chunk['text']}\n"
        
    prompt = f"""
Study material contents:
{context_str}

Instructions:
Create a comprehensive summary of the study material provided above. The summary must be highly structured and optimized for examination preparation.

You must output exactly in this format:

## Chapter Summary

### 1. Main Concepts
* **[Concept 1]**: [Brief description of the concept and why it's important]
* **[Concept 2]**: [Brief description]

### 2. Important Definitions
* **[Term 1]**: [Definition of the term based on the material]
* **[Term 2]**: [Definition]

### 3. Key Points
* [Key point 1 regarding mechanics, workflow, rules, or architecture]
* [Key point 2]

### 4. Quick Revision
* [High-yield summary statements, formulas, or short facts that are quick to memorize for exams]
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction()
        )
    )
    return response.text

def generate_mcq_quiz(context_chunks: list, num_questions: int) -> list:
    """
    Generates a list of multiple-choice questions in JSON format.
    """
    client = get_gemini_client()
    
    context_str = ""
    for chunk in context_chunks:
        context_str += f"\n{chunk['text']}\n"
        
    prompt = f"""
Context study material:
{context_str}

Instructions:
Generate a multiple-choice quiz with exactly {num_questions} questions based on the study material above.
Make the questions educational and directly testing key terms, concepts, and relationships in the material.

You must output a JSON array of objects. Do not wrap the JSON in ```json codeblocks. Return only the raw JSON.
Each object in the array must have the following keys:
- "question": The question text.
- "options": A list of exactly 4 strings (options A, B, C, D).
- "answer": The correct option character: "A", "B", "C", or "D".
- "explanation": A detailed explanation of why the answer is correct and why other options are incorrect.

JSON Example:
[
  {{
    "question": "What is the primary function of TCP?",
    "options": [
      "To route packets across networks",
      "To provide reliable, connection-oriented data transfer",
      "To map IP addresses to MAC addresses",
      "To translate domain names to IP addresses"
    ],
    "answer": "B",
    "explanation": "TCP (Transmission Control Protocol) is responsible for ensuring reliable, ordered, and error-checked delivery of a stream of octets between applications running on hosts communicating over an IP network."
  }}
]
"""
    
    # Configure JSON response type in GenAI SDK
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction(),
            response_mime_type="application/json"
        )
    )
    
    try:
        quiz_data = json.loads(response.text)
        if not isinstance(quiz_data, list):
            raise ValueError("Response is not a list of questions.")
        return quiz_data
    except Exception as e:
        # Fallback parsing in case of code block wrapping
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        try:
            return json.loads(clean_text)
        except Exception:
            raise ValueError(f"Failed to parse generated quiz. Raw response: {response.text}") from e

def generate_exam_questions(context_chunks: list) -> str:
    """
    Generates likely exam questions separated into Short (2-mark), Medium (5-mark), and Long (13/14-mark).
    Answers are not provided.
    """
    client = get_gemini_client()
    
    context_str = ""
    for chunk in context_chunks:
        context_str += f"\n{chunk['text']}\n"
        
    prompt = f"""
Context study material:
{context_str}

Instructions:
Analyze the study material and generate likely college/university examination questions.
Categorize them into three sections:

### Short Questions
(2-mark / short-answer questions. Provide 4-6 questions. Keep them concise and focused on recall/definitions).

### Medium Questions
(5-mark questions. Provide 3-5 questions. Focus on explanations, comparisons, or small processes).

### Long Questions
(13/14-mark questions. Provide 2-3 questions. These should be comprehensive, essay-style questions).

IMPORTANT: Provide ONLY the questions. Do not provide answers in this output.
Format clearly using markdown.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction()
        )
    )
    return response.text

def generate_long_answer(question: str, context_chunks: list) -> str:
    """
    Generates a comprehensive university-exam-style answer using a strict 9-section structure.
    """
    client = get_gemini_client()
    
    context_str = ""
    for i, chunk in enumerate(context_chunks):
        context_str += f"\n--- Section {i+1} ---\n{chunk['text']}\n"
        
    prompt = f"""
Context study material:
{context_str}

Exam Question to answer: {question}

Instructions:
Generate a detailed, structured, university-exam-style answer for the question above, based on the provided study material.
You must use the following exact structure, with clear numbered markdown headings:

### 1. Introduction
(General background of the topic, context, and importance)

### 2. Definition
(Formal, precise definitions of the key terms involved)

### 3. Main Concepts
(Overview of the key components, parameters, or structural parts)

### 4. Detailed Explanation
(Deep-dive explanation of the processes, steps, layers, or mechanics)

### 5. Diagram / Representation
(Provide a clear ASCII text drawing, structured table, or Mermaid flow diagram to visually represent the concept)

### 6. Practical Example
(A concrete real-world example, scenario, or application walkthrough illustrating the concept)

### 7. Advantages
(List and explain key advantages or strengths of this system/concept)

### 8. Applications
(Describe where this concept is used in real-world technology, standards, or systems)

### 9. Conclusion
(A short summary of the key takeaways and examination highlights)

Requirements:
- Write the answer in formal, clear academic language suitable for a college-level examination paper.
- Maximize the use of facts, definitions, and page-references from the provided study material.
- If details for certain sections (like advantages or applications) are not in the study material, you may supplement them using general knowledge, but keep it accurate and realistic. Do not fabricate facts.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction()
        )
    )
    return response.text
