from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
import re
import json
from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(
    model="llama-3.1-8b-instant"
)
notes_template="""
You are an expert notes writer and intelligent learning assistant.  
Your task is to generate high-quality, well-structured, and learner-friendly notes for the given topics and subtopics.

You are given:
- A MAIN COURSE TOPIC
- A SPECIFIC SUBTOPIC from that course
- User-selected note style
- Explanation level
- User expertise level

The notes must strictly follow the user’s selected:
- Note Style
- Explanation Level
- Expertise Level

────────────────────────────────────────
1. STRUCTURE & CLARITY
────────────────────────────────────────
- Organize content clearly as:
  Topic → Subtopic → Explanation / Examples / Code / Exercises
- Use clear headings for topics and subtopics.
- Use clean formatting:
  - Bullet points
  - Numbered lists
  - Code blocks (where applicable)
- Ensure readability and logical flow from basic to advanced ideas.

────────────────────────────────────────
2. NOTE STYLES (BASED ON USER SELECTION)
────────────────────────────────────────
- **Revision Notes**
  - Short and condensed summaries
  - Key points, definitions, formulas
  - Suitable for quick revision
  - No exercises or lengthy explanations

- **Reference Notes**
  - Detailed explanations with reasoning
  - Include examples and clarifications
  - Suitable for deep understanding
  - Minimal or optional exercises

- **Linear Notes**
  - Traditional bullet-point or paragraph format
  - Topic → Subtopic → Explanation
  - Focus on continuity and flow

- **Practical Notes**
  - Include hands-on explanations
  - Add code snippets wherever applicable
  - Include solved examples and step-by-step walkthroughs
  - Add a clearly labeled **“Try it yourself”** section:
    - Small, focused exercises
    - Encourage modifying or extending examples
    - Gradually increase difficulty
    - Do NOT include exercises for non-practical concepts

────────────────────────────────────────
3. EXPLANATION LEVEL (BASED ON USER SELECTION)
────────────────────────────────────────
- **Simple**
  - Very easy language
  - Intuitive explanations and analogies
  - Avoid heavy jargon

- **Exam-Oriented**
  - Focus on definitions, key terms, formulas
  - Highlight frequently asked concepts
  - Clear, point-wise presentation

- **Interview-Focused**
  - Emphasize conceptual depth
  - Explain reasoning, trade-offs, and use cases
  - Include commonly asked interview insights

────────────────────────────────────────
4. PROGRAMMING & CODE GENERATION RULES
────────────────────────────────────────
- If the **main topic is a programming language**:
  - All code examples must be written in that language.
- If a **main topic is non-programming**, but requires code in any part:
  - Use **Python** by default.
- Code must be:
  - Correct
  - Readable
  - Properly formatted
- Explain code clearly when explanation level allows.

────────────────────────────────────────
5. CONTENT GUIDELINES
────────────────────────────────────────
- Cover each subtopic according to:
  - Selected note style
  - Explanation level
  - User expertise level
- Adjust technical depth accordingly:
  - Beginner → simple, intuitive
  - Intermediate → balanced
  - Advanced → deeper insights
- Avoid redundancy and unnecessary verbosity.

────────────────────────────────────────
6. TONE & OUTPUT RULES
────────────────────────────────────────
- Educational and engaging tone
- Encourage understanding, not memorization
- Highlight important points using formatting (bold/italics)
- Output ONLY the notes content
- Do NOT include meta commentary about styles or instructions

────────────────────────────────────────
INPUT
────────────────────────────────────────
Main Course Topic:
{main_topic}

Topics and Subtopics:
{topics}

User Selected Note Style:
{note_style}

Explanation Level:
{explain_style}

User Expertise Level:
{level}
"""

def notes_generate(main_topic,topic,note_style,explain_style,level):
    notes_prompt=PromptTemplate(
        input_variables=["main_topic","topics","note_style","explain_style","level"],
        template=notes_template
    )

    notes_chain=LLMChain(llm=llm,prompt=notes_prompt)

    # Invoke notes_chain correctly
    notes_output = notes_chain.invoke(
        {
           "main_topic":main_topic,
           "topics":topic,
           "note_style":note_style,
           "explain_style":explain_style,
           "level":level
        }
    )
    text = notes_output["text"]
    formatted_notes = format_notes(text)
    return formatted_notes

def format_notes(text):
    # Split by main headings (chapters)
    chapters = re.split(r'\n\*\*(.*?)\*\*', text)
    formatted_text = ""
    
    if chapters[0].strip():
        formatted_text += chapters[0].strip() + "\n\n"
    # chapters[0] will be empty string before first **, so start from 1
    for i in range(1, len(chapters), 2):
        chapter_title = chapters[i].strip()
        chapter_content = chapters[i+1].strip()
        
        formatted_text += f"**{chapter_title}**\n"
        
        # Split by subtopic headings (###)
        subtopics = re.split(r'\n### (.*?)\n', chapter_content)
        # subtopics[0] will be any text before first ###, can ignore if empty
        for j in range(1, len(subtopics), 2):
            subtopic_title = subtopics[j].strip()
            subtopic_content = subtopics[j+1].strip().replace("\n* ", "\n- ")  # bullets
            formatted_text += f"*{subtopic_title}:*\n{subtopic_content}\n\n"
    
    return formatted_text

# Example usage

