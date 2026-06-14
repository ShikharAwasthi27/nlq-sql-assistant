import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"


def load_schema(schema_path="schema.json"):
    with open(schema_path, "r") as f:
        return json.load(f)


def build_prompt(user_question, schema):
    return f"""
You are an expert SQL assistant.

Your task is to convert the user's question into a SQLite SELECT query.

RULES:
1. Generate ONLY SELECT queries.
2. Never generate DELETE, DROP, UPDATE, INSERT, ALTER, or TRUNCATE statements.
3. Use ONLY the tables and columns provided below.
4. Use valid joins based on foreign keys.
5. Return your response ONLY as valid JSON.
6. Do not include markdown formatting.

Database Schema:
{json.dumps(schema, indent=2)}

Return JSON in this format:

{{
    "sql": "<generated_sql>",
    "explanation": "<brief explanation>"
}}

User Question:
{user_question}
"""


def extract_json(response_text):
    """
    Extract JSON even if Gemini wraps it in markdown.
    """

    response_text = response_text.strip()

    response_text = re.sub(
        r"^```json",
        "",
        response_text,
        flags=re.IGNORECASE
    )

    response_text = re.sub(
        r"```$",
        "",
        response_text
    )

    return json.loads(response_text.strip())


def generate_sql(user_question):
    schema = load_schema()

    prompt = build_prompt(user_question, schema)

    model = genai.GenerativeModel(MODEL_NAME)

    response = model.generate_content(prompt)

    result = extract_json(response.text)

    return result


if __name__ == "__main__":

    question = "What are the top 5 selling products by quantity?"

    result = generate_sql(question)

    print("\nGenerated SQL:")
    print(result["sql"])

    print("\nExplanation:")
    print(result["explanation"])
