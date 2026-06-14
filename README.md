# Natural Language to SQL Analytics Assistant (NLQ-to-SQL)

## Overview

This project implements a secure Natural Language to SQL (NLQ-to-SQL) assistant that enables business users to ask questions in plain English and receive SQL-driven insights from a relational database.

The assistant uses Google's Gemini model to convert natural language questions into SQL queries, validates them using SQL guardrails, executes only safe queries, and presents the results through a Streamlit interface.

This project was developed as part of the **Natural Language → SQL Analytics Assistant (NLQ-to-SQL)** assignment.

---

## Features

### Natural Language to SQL Conversion

* Converts English questions into SQL queries using Gemini.
* Uses structured JSON outputs instead of free-text SQL generation.
* Generates a brief explanation of how the SQL answers the question.

### Schema Awareness

* Loads database schema from JSON metadata.
* Restricts SQL generation to known tables and columns.
* Reduces hallucinated table and column names.

### SQL Guardrails

Blocks potentially harmful SQL operations such as:

* DELETE
* DROP
* UPDATE
* ALTER
* TRUNCATE
* INSERT

Additional protections include:

* SELECT-only enforcement
* Semicolon restrictions
* Table validation
* Column validation
* Join validation

### Query Execution

* Executes validated SQL queries on SQLite.
* Uses exception handling for safe execution.
* Logs successful and blocked queries.

### User Interface

* Streamlit-based analytics interface.
* Natural language input box.
* SQL display.
* Query result display.
* Query history sidebar.

### Logging and Evaluation

Logs the following:

* User questions
* Generated SQL
* Validation status
* Execution time
* Number of rows returned
* Error messages

---

## Project Structure

```
nlq_sql_assistant/
│
├── app.py
├── database.py
├── sample_data.py
├── schema_loader.py
├── sql_generator.py
├── guardrails.py
├── logger_util.py
├── requirements.txt
├── .env
├── ecommerce.db
├── schema.json
├── query_logs.csv
└── README.md
```

---

## Technology Stack

| Component              | Technology       |
| ---------------------- | ---------------- |
| Programming Language   | Python           |
| Database               | SQLite           |
| LLM                    | Gemini 2.5 Flash |
| UI                     | Streamlit        |
| SQL Validation         | sqlglot          |
| Data Handling          | pandas           |
| Sample Data Generation | Faker            |
| Environment Variables  | python-dotenv    |

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nlq_sql_assistant
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Gemini API

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

You can obtain a Gemini API key from Google AI Studio.

---

## Generate the Sample Database

Run:

```bash
python sample_data.py
```

This creates:

```
ecommerce.db
```

containing sample e-commerce data.

---

## Generate Schema Metadata

Run:

```bash
python schema_loader.py
```

This creates:

```
schema.json
```

which is used for schema-aware SQL generation and validation.

---

## Test SQL Generation

Run:

```bash
python sql_generator.py
```

Example:

Input:

```
What are the top 5 selling products by quantity?
```

Example Output:

```json
{
    "sql": "SELECT ...",
    "explanation": "..."
}
```

---

## Launch the Streamlit Application

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Example Business Questions

Try the following questions:

* What were the top-selling products last month?
* Which products generated the highest revenue?
* What is the revenue by category?
* Show total orders by city.
* How many customers joined this quarter?
* Which customers placed the most orders?
* What is the average order value?
* Show the total quantity sold for each product.
* Which category has the highest sales?
* List the five most recent orders.

---

## Logging

The application maintains logs in:

```
query_logs.csv
```

Each log entry captures:

* User question
* Generated SQL
* Validation result
* Execution time
* Number of rows returned
* Error messages

---

## Assignment Requirements Covered

### Task 1: Dataset and Schema Preparation

* Multiple related tables
* SQLite database
* Schema metadata generation

### Task 2: Schema Loading and Validation Setup

* Schema loading into Python
* JSON schema representation

### Task 3: NLQ-to-SQL Conversion

* Gemini integration
* Structured JSON outputs
* Schema-aware prompting

### Task 4: SQL Guardrails and Safety Rules

* SELECT-only enforcement
* Harmful SQL blocking
* Table and column validation
* Join validation

### Task 5: Query Execution and Results Display

* SQL execution
* Result rendering
* Explanation generation
* Exception handling

### Task 6: User Interface Development

* Streamlit interface
* Query history
* SQL and result display

### Task 7: Logging and System Evaluation

* Interaction logging
* Validation tracking
* Performance metrics

### Task 8: Documentation and Reporting

* Technical documentation
* Business presentation support

---

## Future Improvements

Potential enhancements include:

* Support for PostgreSQL and MySQL
* Authentication and role-based access control
* Query caching
* Data visualizations and charts
* Conversation history using memory
* More advanced SQL reasoning

---

## Author

Developed as part of the NLQ-to-SQL Analytics Assistant assignment.
