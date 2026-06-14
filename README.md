# Natural Language to SQL Analytics Assistant

A simple NLQ-to-SQL assistant that converts business questions into SQL queries using Gemini, validates them using SQL guardrails, executes safe queries, and displays results.

## Project Structure

```
nlq_sql_assistant/
│
├── sample_data.py
├── schema_loader.py
├── app.py
├── sql_generator.py
├── guardrails.py
├── database.py
├── logger_util.py
├── requirements.txt
├── ecommerce.db
├── schema.json
└── query_logs.csv
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd nlq_sql_assistant
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Generate Database

Run:

```bash
python sample_data.py
```

This creates:

- ecommerce.db

with sample ecommerce data.

## Generate Schema Metadata

Run:

```bash
python schema_loader.py
```

This creates:

- schema.json

used by the NLQ-to-SQL assistant.

## Run the Application

Later parts of this project will introduce Streamlit.

The final application can be launched using:

```bash
streamlit run app.py
```

## Sample Business Questions

- What were the top-selling products last month?
- What is the revenue by category?
- How many customers joined this quarter?
- Which products generated the highest sales?
- Show total orders by city.
