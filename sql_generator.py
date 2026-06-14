import os
import json
import re

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env"
    )

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"


def load_schema(schema_path="schema.json"):
    with open(schema_path, "r") as f:
        return json.load(f)


def build_prompt(user_question, schema):
    return f"""
You are an expert SQLite assistant.

Generate SQL for the user's question.

STRICT RULES:

1. Generate ONLY SELECT statements.
2. Never generate DELETE, DROP, UPDATE,
INSERT, ALTER, TRUNCATE.
3. Use ONLY the schema below.
4. Return ONLY valid JSON.
5. Do NOT wrap output in markdown.

Schema:
{json.dumps(schema, indent=2)}

Return JSON exactly like:

{{
    "sql": "<sql_query>",
    "explanation": "<brief explanation>"
}}

Question:
{user_question}
"""


def extract_json(response_text):
    """
    Extract JSON from Gemini output.
    """

    response_text = response_text.strip()

    response_text = re.sub(
        r"^```json",
        "",
        response_text,
        flags=re.IGNORECASE
    )

    response_text = re.sub(
        r"^```",
        "",
        response_text
    )

    response_text = re.sub(
        r"```$",
        "",
        response_text
    )

    return json.loads(response_text.strip())


def generate_sql(question):
    """
    Returns:
    {
        "sql": "...",
        "explanation": "..."
    }
    """

    schema = load_schema()

    prompt = build_prompt(
        question,
        schema
    )

    model = genai.GenerativeModel(
        MODEL_NAME
    )

    response = model.generate_content(
        prompt
    )

    return extract_json(
        response.text
    )


if __name__ == "__main__":

    question = (
        "What are the top 5 "
        "selling products?"
    )

    result = generate_sql(
        question
    )

    print("\nSQL:")
    print(result["sql"])

    print("\nExplanation:")
    print(result["explanation"])
