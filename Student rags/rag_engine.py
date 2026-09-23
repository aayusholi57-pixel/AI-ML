import os
from pathlib import Path

import pymupdf
from dotenv import load_dotenv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

from openai import OpenAI


# =========================================================
# 1. CONFIGURATION
# =========================================================

DOCUMENTS_DIR = Path(__file__).resolve().parent / "documents"

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# =========================================================
# 2. GEMINI CLIENT
# =========================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not set.\n"
        "Add GOOGLE_API_KEY=YOUR_NEW_GEMINI_API_KEY to E:\\AI-ML\\.env."
    )

client = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Use a currently available Gemini Flash model.
MODEL_NAME = "gemini-2.5-flash"


# =========================================================
# 3. LOAD PDF FILES
# =========================================================

def load_pdfs():

    documents = []

    if not os.path.exists(DOCUMENTS_DIR):

        raise FileNotFoundError(
            f"Folder '{DOCUMENTS_DIR}' was not found."
        )

    for filename in os.listdir(DOCUMENTS_DIR):

        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(
            DOCUMENTS_DIR,
            filename
        )

        print(f"📄 Loading: {filename}")

        pdf = pymupdf.open(pdf_path)

        for page_number, page in enumerate(
            pdf,
            start=1
        ):

            text = page.get_text("text").strip()

            if text:

                documents.append({
                    "source": filename,
                    "page": page_number,
                    "text": text
                })

        pdf.close()

    return documents


# =========================================================
# 4. CREATE CHUNKS
# =========================================================

def create_chunks(
    documents,
    chunk_size=800,
    overlap=100
):

    chunks = []

    for document in documents:

        text = document["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "source": document["source"],
                    "page": document["page"],
                    "text": chunk_text
                })

            start += chunk_size - overlap

    return chunks


# =========================================================
# 5. CREATE TF-IDF + SVD INDEX
# =========================================================

def create_index(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # -----------------------------
    # TF-IDF
    # -----------------------------

    tfidf = TfidfVectorizer(
        stop_words="english",
        max_features=10000
    )

    tfidf_matrix = tfidf.fit_transform(texts)

    # -----------------------------
    # SVD
    # -----------------------------

    max_components = min(
        tfidf_matrix.shape[0] - 1,
        tfidf_matrix.shape[1] - 1,
        100
    )

    if max_components < 1:

        raise ValueError(
            "Not enough data to create SVD index."
        )

    svd = TruncatedSVD(
        n_components=max_components,
        random_state=42
    )

    reduced_matrix = svd.fit_transform(
        tfidf_matrix
    )

    # -----------------------------
    # NORMALIZATION
    # -----------------------------

    normalizer = Normalizer()

    index = normalizer.fit_transform(
        reduced_matrix
    )

    return (
        tfidf,
        svd,
        normalizer,
        index
    )


# =========================================================
# 6. RETRIEVE RELEVANT CHUNKS
# =========================================================

def retrieve(
    question,
    chunks,
    tfidf,
    svd,
    normalizer,
    index,
    k=3
):

    # Question → TF-IDF

    question_tfidf = tfidf.transform(
        [question]
    )

    # TF-IDF → SVD

    question_svd = svd.transform(
        question_tfidf
    )

    # Normalize

    question_vector = normalizer.transform(
        question_svd
    )

    # Cosine similarity
    #
    # Because both vectors are normalized:
    # dot product = cosine similarity

    scores = index @ question_vector[0]

    # Highest score first

    ranked_indices = scores.argsort()[::-1]

    results = []

    for i in ranked_indices[:k]:

        results.append({
            "source": chunks[i]["source"],
            "page": chunks[i]["page"],
            "text": chunks[i]["text"],
            "score": float(scores[i])
        })

    return results


# =========================================================
# 7. BUILD CONTEXT FOR GEMINI
# =========================================================

def build_context(results):

    context_parts = []

    for number, result in enumerate(
        results,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {number}
-------------------------
File: {result['source']}
Page: {result['page']}

{result['text']}
"""
        )

    return "\n".join(context_parts)


# =========================================================
# 8. GENERATE ANSWER WITH GEMINI
# =========================================================

def generate_answer(
    question,
    context,
    mode="explain"
):

    # -----------------------------------------
    # Mode instructions
    # -----------------------------------------

    if mode == "explain":

        mode_instruction = """
Explain the topic clearly for a student.
Use simple language.
Use headings and bullet points where useful.
"""

    elif mode == "short":

        mode_instruction = """
Give a short exam-oriented answer.
Keep it concise but complete.
"""

    elif mode == "5-mark":

        mode_instruction = """
Write a structured 5-mark examination answer.

Include where appropriate:
- Definition
- Main explanation
- Important points
- Example if present in the study material
- Conclusion

Do not add information that is not in the study material.
"""

    elif mode == "mcq":

        mode_instruction = """
Create 5 multiple-choice questions from the
provided study material.

For every question provide:

Question
A.
B.
C.
D.

Correct Answer:
Explanation:

Only use information from the study material.
"""

    else:

        mode_instruction = """
Give a clear exam-oriented answer.
"""


    # -----------------------------------------
    # Prompt
    # -----------------------------------------

    prompt = f"""
You are an Exam Preparation RAG assistant.

Your job is to answer questions using ONLY
the provided study material.

IMPORTANT RULES:

1. Use ONLY the provided study material.
2. Do NOT use outside knowledge.
3. Do NOT invent facts.
4. Do NOT assume missing information.
5. Preserve important technical terminology.
6. If the material does not contain enough
   information, clearly say:

"I couldn't find enough information in the
provided study material."

RESPONSE MODE:
{mode}

MODE INSTRUCTIONS:
{mode_instruction}

STUDY MATERIAL
==================================================

{context}

==================================================

STUDENT QUESTION
==================================================

{question}

==================================================

Now produce the answer.
"""


    # -----------------------------------------
    # Gemini request
    # -----------------------------------------

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise exam preparation "
                    "assistant. Ground every answer in "
                    "the supplied study material."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content


# =========================================================
# 9. COMPLETE EXAM RAG
# =========================================================

def exam_rag(
    question,
    mode="explain",
    k=3
):

    # -----------------------------------------
    # STEP 1 — RETRIEVAL
    # -----------------------------------------

    results = retrieve(
        question,
        chunks,
        tfidf,
        svd,
        normalizer,
        index,
        k=k
    )


    # -----------------------------------------
    # STEP 2 — CONTEXT
    # -----------------------------------------

    context = build_context(
        results
    )


    # -----------------------------------------
    # STEP 3 — GEMINI
    # -----------------------------------------

    answer = generate_answer(
        question,
        context,
        mode=mode
    )


    # -----------------------------------------
    # STEP 4 — RETURN
    # -----------------------------------------

    return {
        "answer": answer,
        "sources": results
    }


# =========================================================
# 10. BUILD KNOWLEDGE BASE
# =========================================================

print()
print("=" * 70)
print("📚 EXAM PREPARATION RAG")
print("=" * 70)

documents = load_pdfs()

print()
print(f"📄 Pages loaded: {len(documents)}")

chunks = create_chunks(
    documents
)

print(
    f"✂️ Chunks created: {len(chunks)}"
)

tfidf, svd, normalizer, index = create_index(
    chunks
)

print(
    f"🧠 Index created: {index.shape}"
)

print()
print("✅ KNOWLEDGE BASE READY")
print("=" * 70)


# =========================================================
# 11. TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    while True:

        print()
        print("=" * 70)

        question = input(
            "Enter your question "
            "(or type 'exit'): "
        ).strip()

        if question.lower() == "exit":

            print("\nGoodbye! 👋")

            break


        # -------------------------------------
        # Select mode
        # -------------------------------------

        print()
        print("Choose mode:")

        print("1. Explain")
        print("2. Short answer")
        print("3. 5-mark answer")
        print("4. MCQs")

        choice = input(
            "\nEnter choice (1-4): "
        ).strip()


        mode_map = {

            "1": "explain",
            "2": "short",
            "3": "5-mark",
            "4": "mcq"

        }

        if choice not in mode_map:

            print(
                "\n❌ Please enter 1, 2, 3, or 4."
            )

            continue


        mode = mode_map[choice]


        # -------------------------------------
        # Run RAG
        # -------------------------------------

        try:

            print()
            print("🔎 Searching study material...")

            result = exam_rag(
                question,
                mode=mode,
                k=3
            )


            # ---------------------------------
            # Answer
            # ---------------------------------

            print()
            print("=" * 70)
            print("🤖 EXAM ANSWER")
            print("=" * 70)

            print(
                result["answer"]
            )


            # ---------------------------------
            # Sources
            # ---------------------------------

            print()
            print("=" * 70)
            print("📚 SOURCES")
            print("=" * 70)

            for source in result["sources"]:

                print(
                    f"📄 {source['source']} "
                    f"| Page {source['page']} "
                    f"| Score: {source['score']:.4f}"
                )


        except Exception as e:

            print()
            print("=" * 70)
            print("❌ ERROR")
            print("=" * 70)

            print(e)