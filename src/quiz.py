import json
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import re
from dotenv import load_dotenv

load_dotenv()

with open(r'D:\ai_course\pages\response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

quiz_template = """
You are an expert MCQ maker.

Generate EXACTLY 10 multiple-choice questions based on the notes below
for a {level} level student.

STRICT RULES:
- Output ONLY valid JSON
- Do NOT add any explanation, heading, or text outside JSON
- Response MUST start with '{{' and end with '}}'
- Follow the JSON structure exactly as shown

Notes:
{Notes}

JSON FORMAT (example only):
{response_json}
"""

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

quiz_prompt=PromptTemplate(
    input_variables=["Notes","level","response_json"],
    template=quiz_template
)

quiz_chains=LLMChain(llm=llm,prompt=quiz_prompt)

def generate_quiz(Notes, level):
    quiz_response = quiz_chains.invoke({
        "Notes": Notes,
        "level": level,
        "response_json": json.dumps(RESPONSE_JSON)
    })

    raw = quiz_response.get("text") or quiz_response.get("output_text")
    if not raw:
        return None

    # clean formatting before parsing
    cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print("Raw text was:", cleaned)
        return None

    
