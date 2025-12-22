from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from dotenv import load_dotenv
import re

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- COURSE GENERATION PROMPT ----------------
TEMPLATE = """
You are an expert AI course designer.

Topic: {topic}
Target Mastery Level: {target_level}

Student Learning Profile:
{student_profile}

Your task:
- Generate a structured list of chapters and subtopics required to reach {target_level} expertise
- Personalize the learning path using the student profile
- Allocate an estimated number of learning hours for each chapter
- Ensure logical progression from foundational concepts to advanced topics

STRICT OUTPUT FORMAT (follow exactly):

**Chapter X: Chapter Title (N hours)**

X.1. Subtopic name
X.2. Subtopic name
X.3. Subtopic name
X.4. Subtopic name

Rules:
- Use sequential chapter numbering starting from Chapter 1
- Use decimal numbering for subtopics (X.1, X.2, ...)
- Do NOT add explanations, summaries, or extra text
- Do NOT use bullet points
- Do NOT skip the hours field
"""


prompt = PromptTemplate(
    input_variables=["topic", "target_level","student_profile"],
    template=TEMPLATE
)

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

topic_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_key="chapters"
)

# ---------------- FORMATTER ----------------
def change_format(text):
    formatted_chapters = []
    chapter_splits = re.split(r"\*\*Chapter (\d+): (.*?)\*\*", text)[1:]

    for i in range(0, len(chapter_splits), 3):
        chap_num = int(chapter_splits[i])
        chap_title = chapter_splits[i + 1].strip()
        chap_body = chapter_splits[i + 2].strip()
        subtopics = re.findall(r"\d+\.\d+\.\s*(.*)", chap_body)

        formatted_chapters.append({
            "chapter": chap_num,
            "title": chap_title,
            "subtopics": subtopics
        })

    return formatted_chapters

# ---------------- SKILL GAP QUESTIONS ----------------
def skill_gap_questions(topic):
    return [
        f"Explain {topic} in your own words.",
        f"What are two important concepts in {topic}?",
        f"Have you implemented or practiced anything related to {topic}? If yes, explain.",
        "Rate your confidence (1–5) in this topic.",
        "Which part of this topic do you find most challenging?"
    ]

# ---------------- LLM-BASED SKILL EVALUATION ----------------
def generate_student_profile(topic, answers):
    llm = ChatGroq(
        model="llama-3.1-8b-instant"
    )
    prompt = f"""
You are an expert learning analyst.

Topic: {topic}

Student responses:
{answers}

Generate a short profile describing:
- Current understanding
- Strengths
- Weak areas
- Learning gaps

Write in 3–5 concise sentences.
Do not include recommendations.
"""

    return llm.invoke(prompt).content.strip()