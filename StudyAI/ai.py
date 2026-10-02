from google import genai
from google.genai import types
import streamlit as st
import json


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_gemini_client():
    """
    Creates and returns the Google Gemini GenAI client.

    The API key is loaded from Streamlit Secrets:
    
    GEMINI_API_KEY = "your_actual_api_key"

    This works with:
    - Local Streamlit: .streamlit/secrets.toml
    - Streamlit Cloud: App Settings -> Secrets
    """

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

    # Check whether API key exists
    if not api_key:
        raise ValueError(
            "Gemini API key is not configured.\n\n"
            "For local development:\n"
            "Create .streamlit/secrets.toml and add:\n\n"
            'GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"\n\n'
            "For Streamlit Cloud:\n"
            "Go to App Settings -> Secrets and add the same value."
        )

    # Check for accidental placeholder
    if api_key == "YOUR_GEMINI_API_KEY_HERE":
        raise ValueError(
            "Gemini API key is still set to the placeholder value.\n\n"
            "Please replace YOUR_GEMINI_API_KEY_HERE "
            "with your actual Gemini API key."
        )

    # Create Gemini client
    return genai.Client(api_key=api_key)


# ============================================================
# SYSTEM INSTRUCTION
# ============================================================

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


# ============================================================
# GROUNDED QUESTION ANSWERING
# ============================================================

def generate_grounded_answer(question: str, context_chunks: list) -> str:
    """
    Generates a Q&A response grounded in retrieved PDF context.
    """

    client = get_gemini_client()

    # Build context string
    context_str = ""

    for i, chunk in enumerate(context_chunks):
        context_str += (
            f"\n--- Context Section {i + 1} "
            f"(Source: {chunk['source']}, Page: {chunk['page']}) ---\n"
        )
        context_str += chunk["text"] + "\n"

    prompt = f"""
Context from student's study material:

{context_str}

Question:
{question}

Instructions:

Answer the student's question based strictly on the provided context sections above.

If the context does not contain the answer, clearly state:

"I couldn't find the answer to this question in your uploaded study material."

Do not invent information.

Ensure your response is structured with:

1. A **Simple Explanation** of the concept in conversational,
   student-friendly language.

2. **Important Points**
   - Bullet points highlighting key mechanics or facts.

3. A concrete **Example**.

4. An **Exam-friendly Explanation** or exam tips where appropriate.

Format the response clearly using markdown headings,
bold text, and bullet points.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction()
        )
    )

    return response.text


# ============================================================
# SIMPLE EXPLANATION
# ============================================================

def explain_simply(concept: str, context_chunks: list) -> str:
    """
    Simplifies a difficult concept using definitions,
    analogies, and practical examples.
    """

    client = get_gemini_client()

    context_str = ""

    for i, chunk in enumerate(context_chunks):
        context_str += (
            f"\n--- Section {i + 1} ---\n"
            f"{chunk['text']}\n"
        )

    prompt = f"""
Context from student's study material:

{context_str}

Concept to explain:
{concept}

Instructions:

Explain this concept in extremely simple,
beginner-friendly terms using the provided context material.

If the concept is not mentioned in the context material,
you can use your general knowledge, but first explicitly state:

*(Note: This concept was not found in your study material,
but here is a simple explanation based on general academic knowledge)*

Structure your response into these exact sections:

### 💡 Simple Definition

Explain the concept in 1-2 sentences using absolutely
no technical jargon, as if explaining to a 10-year-old.

### 🎨 Real-World Analogy

Provide a relatable, vivid real-world analogy.

### ⚙️ Technical Explanation

Provide a brief, clear technical explanation for a college
student and define important terms simply.

### 💻 Practical Example

Show a concrete example, scenario, or walkthrough
where this concept is applied.

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


# ============================================================
# SUMMARY GENERATION
# ============================================================

def generate_summary(context_chunks: list) -> str:
    """
    Summarizes study material in an exam-focused structure.
    """

    client = get_gemini_client()

    context_str = ""

    for chunk in context_chunks:
        context_str += (
            f"\n[Page {chunk['page']}]\n"
            f"{chunk['text']}\n"
        )

    prompt = f"""
Study material contents:

{context_str}

Instructions:

Create a comprehensive summary of the study material
provided above.

The summary must be highly structured and optimized
for examination preparation.

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

* [High-yield summary statements, formulas, or short facts
  that are quick to memorize for exams]
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction()
        )
    )

    return response.text


# ============================================================
# MCQ QUIZ GENERATION
# ============================================================

def generate_mcq_quiz(
    context_chunks: list,
    num_questions: int
) -> list:
    """
    Generates multiple-choice questions in JSON format.
    """

    client = get_gemini_client()

    context_str = ""

    for chunk in context_chunks:
        context_str += f"\n{chunk['text']}\n"

    prompt = f"""
Context study material:

{context_str}

Instructions:

Generate a multiple-choice quiz with exactly
{num_questions} questions based on the study material above.

Make the questions educational and directly test:
- Key terms
- Concepts
- Relationships
- Important facts

You must output a JSON array of objects.

Do not wrap the JSON in a markdown code block.

Return only the raw JSON.

Each object must have these keys:

- "question": The question text.
- "options": A list of exactly 4 strings.
- "answer": The correct option character: "A", "B", "C", or "D".
- "explanation": A detailed explanation of why the answer is correct
  and why the other options are incorrect.

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
    "explanation": "TCP provides reliable and ordered data transfer."
  }}
]
"""

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
            raise ValueError(
                "Response is not a list of questions."
            )

        return quiz_data

    except Exception as e:

        # Fallback parsing
        clean_text = response.text.strip()

        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]

        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]

        clean_text = clean_text.strip()

        try:
            return json.loads(clean_text)

        except Exception:
            raise ValueError(
                f"Failed to parse generated quiz. "
                f"Raw response: {response.text}"
            ) from e


# ============================================================
# EXAM QUESTION GENERATION
# ============================================================

def generate_exam_questions(context_chunks: list) -> str:
    """
    Generates likely examination questions divided into:

    - Short questions
    - Medium questions
    - Long questions
    """

    client = get_gemini_client()

    context_str = ""

    for chunk in context_chunks:
        context_str += f"\n{chunk['text']}\n"

    prompt = f"""
Context study material:

{context_str}

Instructions:

Analyze the study material and generate likely
college/university examination questions.

Categorize them into three sections:

### Short Questions

2-mark / short-answer questions.

Provide 4-6 questions.

Keep them concise and focused on:
- Recall
- Definitions
- Important terms

### Medium Questions

5-mark questions.

Provide 3-5 questions.

Focus on:
- Explanations
- Comparisons
- Small processes

### Long Questions

13/14-mark questions.

Provide 2-3 questions.

These should be comprehensive,
essay-style questions.

IMPORTANT:

Provide ONLY the questions.

Do not provide answers.

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


# ============================================================
# LONG ANSWER GENERATION
# ============================================================

def generate_long_answer(
    question: str,
    context_chunks: list
) -> str:
    """
    Generates a comprehensive university-exam-style answer.
    """

    client = get_gemini_client()

    context_str = ""

    for i, chunk in enumerate(context_chunks):
        context_str += (
            f"\n--- Section {i + 1} ---\n"
            f"{chunk['text']}\n"
        )

    prompt = f"""
Context study material:

{context_str}

Exam Question:

{question}

Instructions:

Generate a detailed, structured,
university-exam-style answer for the question above.

Base the answer on the provided study material.

Use the following exact structure:

### 1. Introduction

General background of the topic,
context, and importance.

### 2. Definition

Formal and precise definitions of
the key terms involved.

### 3. Main Concepts

Overview of the key components,
parameters, or structural parts.

### 4. Detailed Explanation

Deep-dive explanation of the processes,
steps, layers, or mechanics.

### 5. Diagram / Representation

Provide a clear ASCII text drawing,
structured table, or Mermaid flow diagram
to visually represent the concept.

### 6. Practical Example

Provide a concrete real-world example,
scenario, or application walkthrough.

### 7. Advantages

List and explain key advantages
or strengths of the system/concept.

### 8. Applications

Describe where this concept is used
in real-world technology, standards, or systems.

### 9. Conclusion

Provide a short summary of the key takeaways
and examination highlights.

Requirements:

- Write in formal, clear academic language.
- Make it suitable for a college-level examination.
- Maximize the use of facts, definitions,
  and information from the provided study material.
- If details for certain sections such as advantages
  or applications are not available in the study material,
  you may supplement them using general knowledge.
- Do not fabricate facts.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=get_system_instruction()
        )
    )

    return response.text
